"""Types of values to be used in :class:`cion.Field`"""
from cion.exceptions import ValidatorError

__all__ = (
    "string",
    "integer",
)


def string():
    """A string type

    errors if the value is not a string

    Returns:
        InnerValidator: The inner validator
    """

    def inner(value: str):
        if not isinstance(value, str):
            raise ValidatorError("Field must be a valid string")
        return value

    return inner


def integer():
    """An integer type

    errors if the value is not an integer

    Returns:
        InnerValidator: The inner validator
    """

    def inner(value: int):
        if not isinstance(value, int):
            raise ValidatorError("Field must be a valid integer")
        return value

    return inner
