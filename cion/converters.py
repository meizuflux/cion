from typing import Any

from cion import types
from cion.exceptions import ValidatorError

__all__ = (
    "string",
    "integer",
)


def string():
    """Attempts to convert a value to a string

    Most objects can be converted to a string, but if some things override the :meth:`__str__` method, this will not work and will error

    Returns:
        InnerValidator: The inner validator
    """

    def inner(value: Any):
        if not isinstance(value, str):
            try:
                value = str(value)
            except:
                raise ValidatorError("Field must be a valid string")
        return types.string()(value)

    return inner


def integer():
    """Attempts to convert a value to an integer

    Returns:
        InnerValidator: The inner validator
    """

    def inner(value: Any):
        if not isinstance(value, int):
            try:
                value = int(value)
            except:
                raise ValidatorError("Field must be a valid integer")
        return types.integer()(value)

    return inner
