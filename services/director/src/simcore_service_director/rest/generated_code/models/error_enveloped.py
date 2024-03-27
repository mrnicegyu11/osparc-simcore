from .. import util
from .base_model_ import Model
from .inline_response_default_error import InlineResponseDefaultError


class ErrorEnveloped(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, data: object = None, error: InlineResponseDefaultError = None):
        """ErrorEnveloped - a model defined in OpenAPI

        :param data: The data of this ErrorEnveloped.
        :param error: The error of this ErrorEnveloped.
        """
        self.openapi_types = {"data": object, "error": InlineResponseDefaultError}

        self.attribute_map = {"data": "data", "error": "error"}

        self._data = data
        self._error = error

    @classmethod
    def from_dict(cls, dikt: dict) -> "ErrorEnveloped":
        """Returns the dict as a model

        :param dikt: A dict.
        :return: The ErrorEnveloped of this ErrorEnveloped.
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self):
        """Gets the data of this ErrorEnveloped.


        :return: The data of this ErrorEnveloped.
        :rtype: object
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this ErrorEnveloped.


        :param data: The data of this ErrorEnveloped.
        :type data: object
        """

        self._data = data

    @property
    def error(self):
        """Gets the error of this ErrorEnveloped.


        :return: The error of this ErrorEnveloped.
        :rtype: InlineResponseDefaultError
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this ErrorEnveloped.


        :param error: The error of this ErrorEnveloped.
        :type error: InlineResponseDefaultError
        """
        if error is None:
            raise ValueError("Invalid value for `error`, must not be `None`")

        self._error = error
