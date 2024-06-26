import contextlib
import datetime
import logging
from asyncio import Task
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Final
from uuid import uuid4

import redis.asyncio as aioredis
import redis.exceptions
from pydantic import NonNegativeFloat
from pydantic.errors import PydanticErrorMixin
from redis.asyncio.lock import Lock
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from settings_library.redis import RedisDatabase, RedisSettings
from tenacity import retry

from .background_task import periodic_task, start_periodic_task, stop_periodic_task
from .logging_utils import log_catch, log_context
from .retry_policies import RedisRetryPolicyUponInitialization
from .utils import logged_gather

_DEFAULT_LOCK_TTL: Final[datetime.timedelta] = datetime.timedelta(seconds=10)
_DEFAULT_SOCKET_TIMEOUT: Final[datetime.timedelta] = datetime.timedelta(seconds=30)


_logger = logging.getLogger(__name__)


class BaseRedisError(PydanticErrorMixin, RuntimeError):
    ...


class CouldNotAcquireLockError(BaseRedisError):
    msg_template: str = "Lock {lock.name} could not be acquired!"


class CouldNotConnectToRedisError(BaseRedisError):
    msg_template: str = "Connection to '{dsn}' failed"


@dataclass
class RedisClientSDK:
    redis_dsn: str
    _client: aioredis.Redis = field(init=False)

    @property
    def redis(self) -> aioredis.Redis:
        return self._client

    def __post_init__(self):
        self._client = aioredis.from_url(
            self.redis_dsn,
            # Run 3 retries with exponential backoff strategy source: https://redis.readthedocs.io/en/stable/backoff.html
            retry=Retry(ExponentialBackoff(cap=0.512, base=0.008), retries=3),
            retry_on_error=[
                redis.exceptions.BusyLoadingError,
                redis.exceptions.ConnectionError,
                redis.exceptions.TimeoutError,
            ],
            socket_timeout=_DEFAULT_SOCKET_TIMEOUT.total_seconds(),
            socket_connect_timeout=_DEFAULT_SOCKET_TIMEOUT.total_seconds(),
            encoding="utf-8",
            decode_responses=True,
        )

    @retry(**RedisRetryPolicyUponInitialization(_logger).kwargs)
    async def setup(self) -> None:
        if not await self._client.ping():
            await self.shutdown()
            raise CouldNotConnectToRedisError(dsn=self.redis_dsn)
        _logger.info(
            "Connection to %s succeeded with %s",
            f"redis at {self.redis_dsn=}",
            f"{self._client=}",
        )

    async def shutdown(self) -> None:
        await self._client.close(close_connection_pool=True)

    async def ping(self) -> bool:
        with log_catch(_logger, reraise=False):
            await self._client.ping()
            return True
        return False

    @contextlib.asynccontextmanager
    async def lock_context(
        self,
        lock_key: str,
        lock_value: bytes | str | None = None,
        *,
        blocking: bool = False,
        blocking_timeout_s: NonNegativeFloat = 5,
    ) -> AsyncIterator[Lock]:
        """Tries to acquire a lock.

        :param lock_key: unique name of the lock
        :param lock_value: content of the lock, defaults to None
        :param blocking: should block here while acquiring the lock, defaults to False
        :param blocking_timeout_s: time to wait while acquire a lock before giving up, defaults to 5

        :raises CouldNotAcquireLockError: reasons why lock acquisition fails:
            1. `blocking==False` the lock was already acquired by some other entity
            2. `blocking==True` timeouts out while waiting for lock to be free (another entity holds the lock)
        """

        total_lock_duration: datetime.timedelta = _DEFAULT_LOCK_TTL
        lock_unique_id = f"lock_extender_{lock_key}_{uuid4()}"

        ttl_lock: Lock = self._client.lock(
            name=lock_key,
            timeout=total_lock_duration.total_seconds(),
            blocking=blocking,
            blocking_timeout=blocking_timeout_s,
        )

        if not await ttl_lock.acquire(token=lock_value):
            raise CouldNotAcquireLockError(lock=ttl_lock)

        async def _extend_lock(lock: Lock) -> None:
            with log_context(
                _logger, logging.DEBUG, f"Extending lock {lock_unique_id}"
            ), log_catch(_logger, reraise=False):
                await lock.reacquire()

        try:
            async with periodic_task(
                _extend_lock,
                interval=total_lock_duration / 2,
                task_name=lock_unique_id,
                lock=ttl_lock,
                stop_timeout=0.1,
            ):
                # lock is in use now
                yield ttl_lock
        finally:
            # NOTE Why is this error suppressed? Given the following situation:
            # - 250 locks are acquire in parallel with the option `blocking=True`,
            #     meaning: it will wait for the lock to be free before acquiring it
            # - when the lock is acquired the `_extend_lock` task is started
            #     in the background, extending the lock at a fixed interval of time,
            #     which is half of the duration of the lock's TTL
            # - before the task is released the lock extension task is cancelled
            # Here is where the issue occurs:
            # - some time passes between the task's cancellation and
            #     the call to release the lock
            # - if the TTL is too small, 1/2 of the TTL might be just shorter than
            #     the time it passes to between the task is canceled and the task lock is released
            # - this means that the lock will expire and be considered as not owned any longer
            # For example: in one of the failing tests the TTL is set to `0.25` seconds,
            # and half of that is `0.125` seconds.

            # Above implies that only one "task" `owns` and `extends` the lock at a time.
            # The issue appears to be related some timings (being too low).
            try:
                await ttl_lock.release()
            except redis.exceptions.LockNotOwnedError:
                # if this appears outside tests it can cause issues since something might be happening
                _logger.warning(
                    "Attention: lock is no longer owned. This is unexpected and requires investigation"
                )

    async def lock_value(self, lock_name: str) -> str | None:
        output: str | None = await self._client.get(lock_name)
        return output


class RedisClientSDKHealthChecked(RedisClientSDK):
    """
    Provides access to ``is_healthy`` property, to be used for defining
    health check handlers.
    """

    def __init__(
        self,
        redis_dsn: str,
        health_check_interval: datetime.timedelta = datetime.timedelta(seconds=5),
    ) -> None:
        super().__init__(redis_dsn)
        self.health_check_interval: datetime.timedelta = health_check_interval
        self._health_check_task: Task | None = None
        self._is_healthy: bool = True

    @property
    def is_healthy(self) -> bool:
        """Provides the status of Redis.
        If redis becomes available, after being not available,
        it will once more return ``True``

        Returns:
            ``False``: if the service is no longer reachable
            ``True``: when service is reachable
        """
        return self._is_healthy

    async def _check_health(self) -> None:
        self._is_healthy = await self.ping()

    async def setup(self) -> None:
        await super().setup()
        self._health_check_task = start_periodic_task(
            self._check_health,
            interval=self.health_check_interval,
            task_name="redis_service_health_check",
        )

    async def shutdown(self) -> None:
        if self._health_check_task:
            await stop_periodic_task(self._health_check_task)
        await super().shutdown()


@dataclass
class RedisClientsManager:
    """
    Manages the lifetime of redis client sdk connections
    """

    databases: set[RedisDatabase]
    settings: RedisSettings

    _client_sdks: dict[RedisDatabase, RedisClientSDK] = field(default_factory=dict)

    async def setup(self) -> None:
        for db in self.databases:
            self._client_sdks[db] = client_sdk = RedisClientSDK(
                redis_dsn=self.settings.build_redis_dsn(db)
            )
            await client_sdk.setup()

    async def shutdown(self) -> None:
        await logged_gather(*(c.shutdown() for c in self._client_sdks.values()))

    def client(self, database: RedisDatabase) -> RedisClientSDK:
        return self._client_sdks[database]
