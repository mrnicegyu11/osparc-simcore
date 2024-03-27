# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/compose-spec/compose-spec/master/schema/compose-spec.json
#   timestamp: 2021-11-19T10:40:07+00:00

# type:ignore

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConstrainedInt, Extra, Field, conint, constr

#  MODIFICATIONS -------------------------------------------------------------------------
#
#  "$schema": "http://json-schema.org/draft/2019-09/schema#",
#
# UserWarning: format of 'ports' not understood for 'number' - using default
# UserWarning: format of 'ports' not understood for 'string' - using default
# UserWarning: format of 'duration' not understood for 'string' - using default
# UserWarning: format of 'subnet_ip_address' not understood for 'string' - using default


# port number range
class PortInt(ConstrainedInt):
    gt = 0
    lt = 65535


# ----------------------------------------------------------------------------------------


class Configuration(BaseModel):
    class Config:
        extra = Extra.forbid

    source: str | None = None
    target: str | None = None
    uid: str | None = None
    gid: str | None = None
    mode: float | None = None


class CredentialSpec(BaseModel):
    class Config:
        extra = Extra.forbid

    config: str | None = None
    file: str | None = None
    registry: str | None = None


class Condition(Enum):
    service_started = "service_started"
    service_healthy = "service_healthy"
    service_completed_successfully = "service_completed_successfully"


class DependsOn(BaseModel):
    class Config:
        extra = Extra.forbid

    condition: Condition


class Extend(BaseModel):
    class Config:
        extra = Extra.forbid

    service: str
    file: str | None = None


class Logging(BaseModel):
    class Config:
        extra = Extra.forbid

    driver: str | None = None
    options: dict[constr(regex=r"^.+$"), str | float | None] | None = None


class Port(BaseModel):
    class Config:
        extra = Extra.forbid

    mode: str | None = None
    host_ip: str | None = None
    target: int | None = None
    published: int | None = None
    protocol: str | None = None


class PullPolicy(Enum):
    always = "always"
    never = "never"
    if_not_present = "if_not_present"
    build = "build"
    missing = "missing"


class Secret1(BaseModel):
    class Config:
        extra = Extra.forbid

    source: str | None = None
    target: str | None = None
    uid: str | None = None
    gid: str | None = None
    mode: float | None = None


class Ulimit(BaseModel):
    class Config:
        extra = Extra.forbid

    hard: int
    soft: int


class Bind(BaseModel):
    class Config:
        extra = Extra.forbid

    propagation: str | None = None
    create_host_path: bool | None = None


class Volume2(BaseModel):
    class Config:
        extra = Extra.forbid

    nocopy: bool | None = None


class Tmpfs(BaseModel):
    class Config:
        extra = Extra.forbid

    size: conint(ge=0) | str | None = None


class Volume1(BaseModel):
    class Config:
        extra = Extra.forbid

    type: str
    source: str | None = None
    target: str | None = None
    read_only: bool | None = None
    consistency: str | None = None
    bind: Bind | None = None
    volume: Volume2 | None = None
    tmpfs: Tmpfs | None = None


class Healthcheck(BaseModel):
    class Config:
        extra = Extra.forbid

    disable: bool | None = None
    interval: str | None = None
    retries: float | None = None
    test: str | list[str] | None = None
    timeout: str | None = None
    start_period: str | None = None


class Order(Enum):
    start_first = "start-first"
    stop_first = "stop-first"


class RollbackConfig(BaseModel):
    class Config:
        extra = Extra.forbid

    parallelism: int | None = None
    delay: str | None = None
    failure_action: str | None = None
    monitor: str | None = None
    max_failure_ratio: float | None = None
    order: Order | None = None


class Order1(Enum):
    start_first = "start-first"
    stop_first = "stop-first"


class UpdateConfig(BaseModel):
    class Config:
        extra = Extra.forbid

    parallelism: int | None = None
    delay: str | None = None
    failure_action: str | None = None
    monitor: str | None = None
    max_failure_ratio: float | None = None
    order: Order1 | None = None


class Limits(BaseModel):
    class Config:
        extra = Extra.forbid

    cpus: float | str | None = None
    memory: str | None = None


class RestartPolicy(BaseModel):
    class Config:
        extra = Extra.forbid

    condition: str | None = None
    delay: str | None = None
    max_attempts: int | None = None
    window: str | None = None


class Preference(BaseModel):
    class Config:
        extra = Extra.forbid

    spread: str | None = None


class Placement(BaseModel):
    class Config:
        extra = Extra.forbid

    constraints: list[str] | None = None
    preferences: list[Preference] | None = None
    max_replicas_per_node: int | None = None


class DiscreteResourceSpec(BaseModel):
    class Config:
        extra = Extra.forbid

    kind: str | None = None
    value: float | None = None


class GenericResource(BaseModel):
    class Config:
        extra = Extra.forbid

    discrete_resource_spec: DiscreteResourceSpec | None = None


class GenericResources(BaseModel):
    __root__: list[GenericResource]


class ConfigItem(BaseModel):
    class Config:
        extra = Extra.forbid

    subnet: str | None = None
    ip_range: str | None = None
    gateway: str | None = None
    aux_addresses: dict[constr(regex=r"^.+$"), str] | None = None


class Ipam(BaseModel):
    class Config:
        extra = Extra.forbid

    driver: str | None = None
    config: list[ConfigItem] | None = None
    options: dict[constr(regex=r"^.+$"), str] | None = None


class External(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str | None = None


class External1(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str | None = None


class External2(BaseModel):
    name: str | None = None


class External3(BaseModel):
    name: str | None = None


class ListOfStrings(BaseModel):
    __root__: list[str]


class ListOrDict(BaseModel):
    __root__: dict[constr(regex=r".+"), str | float | bool | None] | list[str]


class BlkioLimit(BaseModel):
    class Config:
        extra = Extra.forbid

    path: str | None = None
    rate: int | str | None = None


class BlkioWeight(BaseModel):
    class Config:
        extra = Extra.forbid

    path: str | None = None
    weight: int | None = None


class Constraints(BaseModel):
    __root__: Any


class BuildItem(BaseModel):
    class Config:
        extra = Extra.forbid

    context: str | None = None
    dockerfile: str | None = None
    args: ListOrDict | None = None
    labels: ListOrDict | None = None
    cache_from: list[str] | None = None
    network: str | None = None
    target: str | None = None
    shm_size: int | str | None = None
    extra_hosts: ListOrDict | None = None
    isolation: str | None = None


class BlkioConfig(BaseModel):
    class Config:
        extra = Extra.forbid

    device_read_bps: list[BlkioLimit] | None = None
    device_read_iops: list[BlkioLimit] | None = None
    device_write_bps: list[BlkioLimit] | None = None
    device_write_iops: list[BlkioLimit] | None = None
    weight: int | None = None
    weight_device: list[BlkioWeight] | None = None


class Network1(BaseModel):
    class Config:
        extra = Extra.forbid

    aliases: ListOfStrings | None = None
    ipv4_address: str | None = None
    ipv6_address: str | None = None
    link_local_ips: ListOfStrings | None = None
    priority: float | None = None


class Device(BaseModel):
    class Config:
        extra = Extra.forbid

    capabilities: ListOfStrings | None = None
    count: str | int | None = None
    device_ids: ListOfStrings | None = None
    driver: str | None = None
    options: ListOrDict | None = None


class Devices(BaseModel):
    __root__: list[Device]


class Network(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str | None = None
    driver: str | None = None
    driver_opts: dict[constr(regex=r"^.+$"), str | float] | None = None
    ipam: Ipam | None = None
    external: External | None = None
    internal: bool | None = None
    enable_ipv6: bool | None = None
    attachable: bool | None = None
    labels: ListOrDict | None = None


class Volume(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str | None = None
    driver: str | None = None
    driver_opts: dict[constr(regex=r"^.+$"), str | float] | None = None
    external: External1 | None = None
    labels: ListOrDict | None = None


class Secret(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str | None = None
    file: str | None = None
    external: External2 | None = None
    labels: ListOrDict | None = None
    driver: str | None = None
    driver_opts: dict[constr(regex=r"^.+$"), str | float] | None = None
    template_driver: str | None = None


class ComposeSpecConfig(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str | None = None
    file: str | None = None
    external: External3 | None = None
    labels: ListOrDict | None = None
    template_driver: str | None = None


class StringOrList(BaseModel):
    __root__: str | ListOfStrings


class Reservations(BaseModel):
    class Config:
        extra = Extra.forbid

    cpus: float | str | None = None
    memory: str | None = None
    generic_resources: GenericResources | None = None
    devices: Devices | None = None


class Resources(BaseModel):
    class Config:
        extra = Extra.forbid

    limits: Limits | None = None
    reservations: Reservations | None = None


class Deployment(BaseModel):
    class Config:
        extra = Extra.forbid

    mode: str | None = None
    endpoint_mode: str | None = None
    replicas: int | None = None
    labels: ListOrDict | None = None
    rollback_config: RollbackConfig | None = None
    update_config: UpdateConfig | None = None
    resources: Resources | None = None
    restart_policy: RestartPolicy | None = None
    placement: Placement | None = None


class Service(BaseModel):
    class Config:
        extra = Extra.forbid

    deploy: Deployment | None = None
    build: str | BuildItem | None = None
    blkio_config: BlkioConfig | None = None
    cap_add: list[str] | None = None
    cap_drop: list[str] | None = None
    cgroup_parent: str | None = None
    command: str | list[str] | None = None
    configs: list[str | Configuration] | None = None
    container_name: str | None = None
    cpu_count: conint(ge=0) | None = None
    cpu_percent: conint(ge=0, le=100) | None = None
    cpu_shares: float | str | None = None
    cpu_quota: float | str | None = None
    cpu_period: float | str | None = None
    cpu_rt_period: float | str | None = None
    cpu_rt_runtime: float | str | None = None
    cpus: float | str | None = None
    cpuset: str | None = None
    credential_spec: CredentialSpec | None = None
    depends_on: None | (
        ListOfStrings | dict[constr(regex=r"^[a-zA-Z0-9._-]+$"), DependsOn]
    ) = None
    device_cgroup_rules: ListOfStrings | None = None
    devices: list[str] | None = None
    dns: StringOrList | None = None
    dns_opt: list[str] | None = None
    dns_search: StringOrList | None = None
    domainname: str | None = None
    entrypoint: str | list[str] | None = None
    env_file: StringOrList | None = None
    environment: ListOrDict | None = None
    expose: list[str | float] | None = None
    extends: str | Extend | None = None
    external_links: list[str] | None = None
    extra_hosts: ListOrDict | None = None
    group_add: list[str | float] | None = None
    healthcheck: Healthcheck | None = None
    hostname: str | None = None
    image: str | None = None
    init: bool | None = None
    ipc: str | None = None
    isolation: str | None = None
    labels: ListOrDict | None = None
    links: list[str] | None = None
    logging: Logging | None = None
    mac_address: str | None = None
    mem_limit: float | str | None = None
    mem_reservation: str | int | None = None
    mem_swappiness: int | None = None
    memswap_limit: float | str | None = None
    network_mode: str | None = None
    networks: None | (
        ListOfStrings | dict[constr(regex=r"^[a-zA-Z0-9._-]+$"), Network1 | None]
    ) = None
    oom_kill_disable: bool | None = None
    oom_score_adj: conint(ge=-1000, le=1000) | None = None
    pid: str | None | None = None
    pids_limit: float | str | None = None
    platform: str | None = None
    ports: list[PortInt | str | Port] | None = None
    privileged: bool | None = None
    profiles: ListOfStrings | None = None
    pull_policy: PullPolicy | None = None
    read_only: bool | None = None
    restart: str | None = None
    runtime: str | None = None
    scale: int | None = None
    security_opt: list[str] | None = None
    shm_size: float | str | None = None
    secrets: list[str | Secret1] | None = None
    sysctls: ListOrDict | None = None
    stdin_open: bool | None = None
    stop_grace_period: str | None = None
    stop_signal: str | None = None
    storage_opt: dict[str, Any] | None = None
    tmpfs: StringOrList | None = None
    tty: bool | None = None
    ulimits: dict[constr(regex=r"^[a-z]+$"), int | Ulimit] | None = None
    user: str | None = None
    userns_mode: str | None = None
    volumes: list[str | Volume1] | None = None
    volumes_from: list[str] | None = None
    working_dir: str | None = None


class ComposeSpecification(BaseModel):
    """
    The Compose file is a YAML file defining a multi-containers based application.
    """

    class Config:
        extra = Extra.forbid

    version: str | None = Field(
        None,
        description="Version of the Compose specification used. Tools not implementing required version MUST reject the configuration file.",
    )
    services: dict[constr(regex=r"^[a-zA-Z0-9._-]+$"), Service] | None = None
    networks: dict[constr(regex=r"^[a-zA-Z0-9._-]+$"), Network] | None = None
    volumes: dict[constr(regex=r"^[a-zA-Z0-9._-]+$"), Volume] | None = None
    secrets: dict[constr(regex=r"^[a-zA-Z0-9._-]+$"), Secret] | None = None
    configs: None | (dict[constr(regex=r"^[a-zA-Z0-9._-]+$"), ComposeSpecConfig]) = None
