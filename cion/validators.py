from typing import Any, Callable, Iterable, Optional
from uuid import UUID

from cion.exceptions import ValidatorError

__all__ = (
    "length",
    "one_of",
)

InnerValidator = Callable[[Any], Any]


def length(
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    *,
    equal_to: Optional[int] = None,
    base_error_message: str = "Length must be ",
    error_messages: Optional[dict[str, str]] = None,
) -> InnerValidator:
    """Validates the length of a string

    The type of the value to be validated is not enforced as :obj:`str`
    Used as a constraint on a field with :class:`cion.Schema`

    Args:
        minimum (int): The minimum length that the string can be
        maximum (int): The maximum length that the string can be
        equal_to (int): A number that the length of the string must equal.
            Cannot be used with minimum and maximum
        base_error_message (str): The start of the error message. View source for exact example
        error_messages (dict):
            A dictionary of the error messages that are allowed to be raised.

            If ``equal_to`` is specified, then the ``equal_to`` key is used and added on after ``base_error_message``

            If ``minimum`` or ``maximum`` is specified, then the respective key is used and added on after ``base_error_message``

            If both ``minimum`` and ``maximum`` are specified, then minimum and maximum error message is added together with ``and`` and then that is added on after ``base_error_message``

    Note:
        The error message implementation is a bit complicated for this validator, it is recommended that you look at the source code for this function for more information

    Returns:
        InnerValidator: The inner function that is called when validating schema
    """
    error_message = base_error_message
    _error_messages = {
        "equal_to": "equal to {equal_to}",
        "minimum": "greater than {minimum}",
        "maximum": "less than {maximum}",
    }
    _error_messages.update(error_messages or {})
    if equal_to is not None:
        error_message += _error_messages["equal_to"].format(equal_to=equal_to)
    else:
        if minimum is not None and maximum is not None:
            error_message += _error_messages.get(
                "both",
                (f"{_error_messages['minimum']} and {_error_messages['maximum']}").format(
                    minimum=minimum, maximum=maximum, equal_to=equal_to
                ),
            )
        elif minimum is not None:
            error_message += _error_messages["minimum"].format(minimum=minimum)
        elif maximum is not None:
            error_message += _error_messages["maximum"].format(maximum=maximum)

    def inner(value: str):
        if equal_to is None:
            if minimum is not None and len(value) < minimum:
                raise ValidatorError(error_message)
            if maximum is not None and len(value) > maximum:
                raise ValidatorError(error_message)
        elif len(value) != equal_to:
            raise ValidatorError(error_message)

        return value

    return inner


def range(
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    error_message: str = "Number must be between {minimum} and {maximum}",
) -> InnerValidator:
    """Validates that a number is in a range

    The type of the value to be validated is not enforced as :obj:`int`
    Used as a constraint on a field with :class:`cion.Schema`

    Args:
        minimum (int): The minimum length that the number can be
        maximum (int): The maximum length that the number can be
        error_message (str): The error message that is raised
            You can use the ``minimum`` and ``maximum`` variables in the error message

    Returns:
        InnerValidator: The inner function that is called when validating schema
    """

    def inner(value: int):
        if minimum is not None and value < minimum:
            raise ValidatorError(error_message.format(minimum=minimum, maximum=maximum or "infinity"))
        if maximum is not None and value > maximum:
            raise ValidatorError(error_message.format(minimum=minimum or "0", maximum=maximum))

        return value

    return inner


def one_of(values: Iterable[Any], error_message: str = "Value must be one of {values}") -> InnerValidator:
    """Checks if the value is in a list of values

    Used as a constraint on a field with :class:`cion.Schema`
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


def not_one_of(values: Iterable[Any], error_message: str = "Value must not be one of {values}") -> InnerValidator:
    """Checks if the value is not in a list of values

    Used as a constraint on a field with :class:`cion.Schema`
    No assumptions are made about the type of the value

    Args:
        values: An iterable containing valid values
        error_message (str): The error message that is raised
            The `values` variable can be used, and it is the values joined together by a string

    Returns:
        InnerValidator: The inner function that is called when validating schema
    """

    def inner(value: Any):
        if value in values:
            raise ValidatorError(error_message.format(values=", ".join(str(v) for v in values)))
        return value

    return inner


def equal_to(value_: Any, error_message: str = "Must be equal to {equal_to}") -> InnerValidator:
    """Validator that ensures a value is equal to a certain value

    No assumptions are made about types of any kind

    Args:
        value_: The item that the value must be equal to
        error_message: The error message that is raised when the value does not validate properly.
            You can use the ``equal_to`` variable in the message

    """

    def inner(value: Any) -> Any:
        if value != value_:
            raise ValidatorError(error_message.format(equal_to=str(equal_to)))

        return value

    return inner


def uuid(error_message: str = "Must be a valid UUID", **kwargs) -> InnerValidator:
    def inner(value: str) -> UUID:
        try:
            transformed = UUID(value, **kwargs)
        except (ValueError, AttributeError, TypeError):
            raise ValidatorError(error_message)
        return transformed

    return inner
