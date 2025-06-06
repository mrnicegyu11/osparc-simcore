from collections.abc import AsyncIterator
from typing import cast

from fastapi import FastAPI
from fastapi_lifespan_manager import State
from models_library.rabbitmq_messages import RabbitMessageBase
from servicelib.rabbitmq import (
    RabbitMQClient,
    RabbitMQRPCClient,
    wait_till_rabbitmq_responsive,
)
from settings_library.rabbit import RabbitSettings


async def rabbitmq_lifespan(app: FastAPI) -> AsyncIterator[State]:
    settings: RabbitSettings = app.state.settings.DYNAMIC_SCHEDULER_RABBITMQ

    await wait_till_rabbitmq_responsive(settings.dsn)

    app.state.rabbitmq_client = RabbitMQClient(
        client_name="dynamic_scheduler", settings=settings
    )
    app.state.rabbitmq_rpc_client = await RabbitMQRPCClient.create(
        client_name="dynamic_scheduler_rpc_client", settings=settings
    )
    app.state.rabbitmq_rpc_server = await RabbitMQRPCClient.create(
        client_name="dynamic_scheduler_rpc_server", settings=settings
    )

    yield {}

    await app.state.rabbitmq_client.close()
    await app.state.rabbitmq_rpc_client.close()
    await app.state.rabbitmq_rpc_server.close()


def get_rabbitmq_client(app: FastAPI) -> RabbitMQClient:
    assert app.state.rabbitmq_client  # nosec
    return cast(RabbitMQClient, app.state.rabbitmq_client)


def get_rabbitmq_rpc_client(app: FastAPI) -> RabbitMQRPCClient:
    assert app.state.rabbitmq_rpc_client
    return cast(RabbitMQRPCClient, app.state.rabbitmq_rpc_client)


def get_rabbitmq_rpc_server(app: FastAPI) -> RabbitMQRPCClient:
    assert app.state.rabbitmq_rpc_server  # nosec
    return cast(RabbitMQRPCClient, app.state.rabbitmq_rpc_server)


async def post_message(app: FastAPI, message: RabbitMessageBase) -> None:
    await get_rabbitmq_client(app).publish(message.channel_name, message)
