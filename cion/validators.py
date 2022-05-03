from typing import Any, Callable, Iterable

from cion.exceptions import ValidatorError

InnerValidator = Callable[[Any], Any]


def length(
    minimum: int, maximum: int, error_message: str = "Length must be between {minimum} and {maximum}"
) -> InnerValidator:
    """Validates the length of a string

    The type of the value to be validated is not enforced as :obj:`str`
    Used as a constraint on a field with :class:`.Schema`

    Args:
        minimum (int): The minimum length that the string can be
        maximum (int): The maximum length that the string can be
        error_message (str): The error message that is raised
            The error message is formatted like `error_message.format(minimum=minimum, maximum=maximum)`

    Returns:
        InnerValidator: The inner function that is called when validating schema
    """

    def inner(value: str):
        if len(value) < minimum or len(value) > maximum:
            raise ValidatorError(error_message.format(minimum=minimum, maximum=maximum))
        return value

    return inner


def one_of(values: Iterable[Any], error_message: str = "Value must be one of {values}") -> InnerValidator:
    """Checks if the value is in a list of values

    Used as a constraint on a field with :class:`.Schema`
    No assumptions are made about the type of the value

    Args:
        values: An iterable containing valid values
        error_message (str): The error message that is raised
            The `values` variable can be used, and it is the values joined together by a string

    Returns:
        InnerValidator: The inner function that is called when validating schema
    """

    def inner(value: Any):
        if value not in values:
            raise ValidatorError(error_message.format(values=", ".join(str(v) for v in values)))
        return value

    return inner
