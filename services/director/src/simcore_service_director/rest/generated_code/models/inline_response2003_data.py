import re

from .. import util
from .base_model_ import Model


class InlineResponse2003Data(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(
        self,
        published_port: int = None,
        entry_point: str = None,
        service_uuid: str = None,
        service_key: str = None,
        service_version: str = None,
        service_host: str = None,
        service_port: int = None,
        service_basepath: str = "",
        service_state: str = None,
        service_message: str = None,
        user_id: str = None,
    ):
        """InlineResponse2003Data - a model defined in OpenAPI

        :param published_port: The published_port of this InlineResponse2003Data.
        :param entry_point: The entry_point of this InlineResponse2003Data.
        :param service_uuid: The service_uuid of this InlineResponse2003Data.
        :param service_key: The service_key of this InlineResponse2003Data.
        :param service_version: The service_version of this InlineResponse2003Data.
        :param service_host: The service_host of this InlineResponse2003Data.
        :param service_port: The service_port of this InlineResponse2003Data.
        :param service_basepath: The service_basepath of this InlineResponse2003Data.
        :param service_state: The service_state of this InlineResponse2003Data.
        :param service_message: The service_message of this InlineResponse2003Data.
        :param user_id: The user_id of this InlineResponse2003Data.
        """
        self.openapi_types = {
            "published_port": int,
            "entry_point": str,
            "service_uuid": str,
            "service_key": str,
            "service_version": str,
            "service_host": str,
            "service_port": int,
            "service_basepath": str,
            "service_state": str,
            "service_message": str,
            "user_id": str,
        }

        self.attribute_map = {
            "published_port": "published_port",
            "entry_point": "entry_point",
            "service_uuid": "service_uuid",
            "service_key": "service_key",
            "service_version": "service_version",
            "service_host": "service_host",
            "service_port": "service_port",
            "service_basepath": "service_basepath",
            "service_state": "service_state",
            "service_message": "service_message",
            "user_id": "user_id",
        }

        self._published_port = published_port
        self._entry_point = entry_point
        self._service_uuid = service_uuid
        self._service_key = service_key
        self._service_version = service_version
        self._service_host = service_host
        self._service_port = service_port
        self._service_basepath = service_basepath
        self._service_state = service_state
        self._service_message = service_message
        self._user_id = user_id

    @classmethod
    def from_dict(cls, dikt: dict) -> "InlineResponse2003Data":
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The inline_response_200_3_data of this InlineResponse2003Data.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def published_port(self):
        """Gets the published_port of this InlineResponse2003Data.

        The ports where the service provides its interface

        :return: The published_port of this InlineResponse2003Data.
        :rtype: int
        """
        return self._published_port

    @published_port.setter
    def published_port(self, published_port):
        """Sets the published_port of this InlineResponse2003Data.

        The ports where the service provides its interface

        :param published_port: The published_port of this InlineResponse2003Data.
        :type published_port: int
        """
        if published_port is None:
            raise ValueError("Invalid value for `published_port`, must not be `None`")
        if published_port is not None and published_port < 1:
            raise ValueError(
                "Invalid value for `published_port`, must be a value greater than or equal to `1`"
            )

        self._published_port = published_port

    @property
    def entry_point(self):
        """Gets the entry_point of this InlineResponse2003Data.

        The entry point where the service provides its interface if specified

        :return: The entry_point of this InlineResponse2003Data.
        :rtype: str
        """
        return self._entry_point

    @entry_point.setter
    def entry_point(self, entry_point):
        """Sets the entry_point of this InlineResponse2003Data.

        The entry point where the service provides its interface if specified

        :param entry_point: The entry_point of this InlineResponse2003Data.
        :type entry_point: str
        """

        self._entry_point = entry_point

    @property
    def service_uuid(self):
        """Gets the service_uuid of this InlineResponse2003Data.

        The UUID attached to this service

        :return: The service_uuid of this InlineResponse2003Data.
        :rtype: str
        """
        return self._service_uuid

    @service_uuid.setter
    def service_uuid(self, service_uuid):
        """Sets the service_uuid of this InlineResponse2003Data.

        The UUID attached to this service

        :param service_uuid: The service_uuid of this InlineResponse2003Data.
        :type service_uuid: str
        """
        if service_uuid is None:
            raise ValueError("Invalid value for `service_uuid`, must not be `None`")

        self._service_uuid = service_uuid

    @property
    def service_key(self):
        """Gets the service_key of this InlineResponse2003Data.

        distinctive name for the node based on the docker registry path

        :return: The service_key of this InlineResponse2003Data.
        :rtype: str
        """
        return self._service_key

    @service_key.setter
    def service_key(self, service_key):
        """Sets the service_key of this InlineResponse2003Data.

        distinctive name for the node based on the docker registry path

        :param service_key: The service_key of this InlineResponse2003Data.
        :type service_key: str
        """
        if service_key is None:
            raise ValueError("Invalid value for `service_key`, must not be `None`")
        if service_key is not None and not re.search(
            r"^simcore/services/"
            r"(?P<type>(comp|dynamic|frontend))/"
            r"(?P<subdir>[a-z0-9][a-z0-9_.-]*/)*"
            r"(?P<name>[a-z0-9-_]+[a-z0-9])$",
            service_key,
        ):
            raise ValueError(
                r"Invalid value for `service_key`, must be a follow pattern or equal to `/^(simcore)\/(services)\/(comp|dynamic)(\/[\w\/-]+)+$/`"
            )

        self._service_key = service_key

    @property
    def service_version(self):
        """Gets the service_version of this InlineResponse2003Data.

        semantic version number

        :return: The service_version of this InlineResponse2003Data.
        :rtype: str
        """
        return self._service_version

    @service_version.setter
    def service_version(self, service_version):
        """Sets the service_version of this InlineResponse2003Data.

        semantic version number

        :param service_version: The service_version of this InlineResponse2003Data.
        :type service_version: str
        """
        if service_version is None:
            raise ValueError("Invalid value for `service_version`, must not be `None`")
        if service_version is not None and not re.search(
            r"^(0|[1-9]\d*)(\.(0|[1-9]\d*)){2}(-(0|[1-9]\d*|\d*[-a-zA-Z][-\da-zA-Z]*)(\.(0|[1-9]\d*|\d*[-a-zA-Z][-\da-zA-Z]*))*)?(\+[-\da-zA-Z]+(\.[\da-zA-Z-]+)*)?$",
            service_version,
        ):
            raise ValueError(
                r"Invalid value for `service_version`, must be a follow pattern or equal to `/^(0|[1-9]\d*)(\.(0|[1-9]\d*)){2}(-(0|[1-9]\d*|\d*[-a-zA-Z][-\da-zA-Z]*)(\.(0|[1-9]\d*|\d*[-a-zA-Z][-\da-zA-Z]*))*)?(\+[-\da-zA-Z]+(\.[-\da-zA-Z-]+)*)?$/`"
            )

        self._service_version = service_version

    @property
    def service_host(self):
        """Gets the service_host of this InlineResponse2003Data.

        service host name within the network

        :return: The service_host of this InlineResponse2003Data.
        :rtype: str
        """
        return self._service_host

    @service_host.setter
    def service_host(self, service_host):
        """Sets the service_host of this InlineResponse2003Data.

        service host name within the network

        :param service_host: The service_host of this InlineResponse2003Data.
        :type service_host: str
        """
        if service_host is None:
            raise ValueError("Invalid value for `service_host`, must not be `None`")

        self._service_host = service_host

    @property
    def service_port(self):
        """Gets the service_port of this InlineResponse2003Data.

        port to access the service within the network

        :return: The service_port of this InlineResponse2003Data.
        :rtype: int
        """
        return self._service_port

    @service_port.setter
    def service_port(self, service_port):
        """Sets the service_port of this InlineResponse2003Data.

        port to access the service within the network

        :param service_port: The service_port of this InlineResponse2003Data.
        :type service_port: int
        """
        if service_port is None:
            raise ValueError("Invalid value for `service_port`, must not be `None`")
        if service_port is not None and service_port < 1:
            raise ValueError(
                "Invalid value for `service_port`, must be a value greater than or equal to `1`"
            )

        self._service_port = service_port

    @property
    def service_basepath(self):
        """Gets the service_basepath of this InlineResponse2003Data.

        different base path where current service is mounted otherwise defaults to root

        :return: The service_basepath of this InlineResponse2003Data.
        :rtype: str
        """
        return self._service_basepath

    @service_basepath.setter
    def service_basepath(self, service_basepath):
        """Sets the service_basepath of this InlineResponse2003Data.

        different base path where current service is mounted otherwise defaults to root

        :param service_basepath: The service_basepath of this InlineResponse2003Data.
        :type service_basepath: str
        """

        self._service_basepath = service_basepath

    @property
    def service_state(self):
        """Gets the service_state of this InlineResponse2003Data.

        the service state * 'pending' - The service is waiting for resources to start * 'pulling' - The service is being pulled from the registry * 'starting' - The service is starting * 'running' - The service is running * 'complete' - The service completed * 'failed' - The service failed to start

        :return: The service_state of this InlineResponse2003Data.
        :rtype: str
        """
        return self._service_state

    @service_state.setter
    def service_state(self, service_state):
        """Sets the service_state of this InlineResponse2003Data.

        the service state * 'pending' - The service is waiting for resources to start * 'pulling' - The service is being pulled from the registry * 'starting' - The service is starting * 'running' - The service is running * 'complete' - The service completed * 'failed' - The service failed to start

        :param service_state: The service_state of this InlineResponse2003Data.
        :type service_state: str
        """
        allowed_values = [
            "pending",
            "pulling",
            "starting",
            "running",
            "complete",
            "failed",
        ]
        if service_state not in allowed_values:
            raise ValueError(
                "Invalid value for `service_state` ({}), must be one of {}".format(
                    service_state, allowed_values
                )
            )

        self._service_state = service_state

    @property
    def service_message(self):
        """Gets the service_message of this InlineResponse2003Data.

        the service message

        :return: The service_message of this InlineResponse2003Data.
        :rtype: str
        """
        return self._service_message

    @service_message.setter
    def service_message(self, service_message):
        """Sets the service_message of this InlineResponse2003Data.

        the service message

        :param service_message: The service_message of this InlineResponse2003Data.
        :type service_message: str
        """

        self._service_message = service_message

    @property
    def user_id(self):
        """Gets the user_id of this InlineResponse2003Data.

        the user that started the service

        :return: The user_id of this InlineResponse2003Data.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this InlineResponse2003Data.

        the user that started the service

        :param user_id: The user_id of this InlineResponse2003Data.
        :type user_id: str
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")

        self._user_id = user_id
