"""Types of values to be used in :class:`cion.Field`"""
from cion.exceptions import ValidatorError

__all__ = (
    "string",
    "integer",
)


def string(cast: bool = True):
    """A string type

    Used when defining fields in :class:`cion.Schema`

    Args:
        cast (bool): Whether or not to try to cast the value to a :obj:`str`

    Returns:
        InnerValidator: The inner validator
    """

    def inner(value: str):
        if not isinstance(value, str):
            if cast:
                try:
                    value = str(value)
                except:
                    raise ValidatorError("Field must be a valid string")
            else:
                raise ValidatorError("Field must be a valid string")
        return value

    return inner


def integer(cast: bool = False):
    """An integer type

    Used when defining fields in :class:`cion.Schema`

    Args:
        cast (bool): Whether or not to try to cast the value to an :obj:`int`

    Returns:
        InnerValidator: The inner validator
    """

    def inner(value: int):
        if not isinstance(value, int):
            if cast:
                try:
                    value = int(value)
                except:
                    raise ValidatorError("Field must be a valid string")
            else:
                raise ValidatorError("Field must be a valid integer")
        return value

    return inner
