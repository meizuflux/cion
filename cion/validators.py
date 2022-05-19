"""Validators for use in a :class:`cion.Field`"""
import re
from typing import Any, Callable, Iterable, Literal, Optional
from uuid import UUID

from cion.exceptions import ValidatorError

__all__ = (
    "length",
    "range_",
    "one_of",
    "not_one_of",
    "equal_to",
    "uuid",
    "regex",
    "url",
    "email",
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
    """Validates the length of a value

    This can be a string, list, or something like a dictionary, or basically any iterable
    (anything that len(value) can be called on)

    Args:
        minimum (int): The minimum length that the value can be
        maximum (int): The maximum length that the value can be
        equal_to (int): A number that the length of the value must equal.
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


def range_(
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    error_message: str = "Number must be between {minimum} and {maximum}",
) -> InnerValidator:
    """Validates that a number is in a range

    Args:
        minimum (int): The minimum length that the number can be
        maximum (int): The maximum length that the number can be
        error_message (str): The error message that is raised
            You can use the ``minimum`` and ``maximum`` variables in the error message
    """

    def inner(value: int):
        if minimum is not None and value < minimum:
            raise ValidatorError(error_message.format(minimum=minimum, maximum=maximum or "infinity"))
        if maximum is not None and value > maximum:
            raise ValidatorError(error_message.format(minimum=minimum or "0", maximum=maximum))

        return value

    return inner


def one_of(*values: Any, error_message: str = "Value must be one of {values}") -> InnerValidator:
    """Checks if the value is in a list of values

    Used as a constraint on a field with :class:`cion.Schema`
    No assumptions are made about the type of the value

    Args:
        values: Any non-keyword arguments are valid values
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


def not_one_of(*values: Iterable[Any], error_message: str = "Value must not be one of {values}") -> InnerValidator:
    """Checks if the value is not in a list of values

    Used as a constraint on a field with :class:`cion.Schema`
    No assumptions are made about the type of the value

    Args:
        values: Any non-keyword arguments are valid values
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


def regex(
    pattern: str,
    *,
    cast: bool = False,
    function: Literal["match", "fullmatch", "search"] = "fullmatch",
    flags: Any = 0,
    error_message="Must match regex",
    **kwargs: Any,
) -> InnerValidator:
    """Match a value against a regex pattern

    Note:
        It is highly recommended that you customize the error message, as regex functions tend to be application specific, and not generic.


    Args:
        pattern: The regex pattern that you want to match a string against
        cast: The value is always casted to a string, but if you wish to preserve the initial value, set this to ``False``
        function (One of ``match``, ``fullmatch``, ``search``): What regex function to use against the value.
            View the regex docs for information about these https://docs.python.org/3/library/re.html#re.fullmatch

            TL,DR: Match matches at the start, fullmatch matches the entire string, and search searches the string for something to match
        flags: Flags to pass to :meth:``re.compile``.
            https://docs.python.org/3/library/re.html#re.A
        error_message: The error message raised when the match object returned when matching is None.
        kwargs: Arguments to pass to the method used for matching (again, see regex docs related to the function)

    """
    prog = re.compile(pattern, flags=flags)
    to_call = getattr(prog, function)

    def inner(value: str) -> Any:
        casted = str(value)
        match = to_call(casted, **kwargs)
        if match is None:
            raise ValidatorError(error_message)

        return casted if cast is True else value

    return inner


def url(schemes: list[str] = ["http", "https"], *, error_message: str = "Must be a valid URL") -> InnerValidator:
    """Validates that a value is a valid URL

    This implementation uses :func:`regex` under the hood

    Args:
        schemes: A list of http schemes that will be valid
        error_message: The error message to raise if a value is not a valid URL
    """

    return regex(
        rf"({'|'.join(schemes)}):\/\/[-a-zA-Z0-9@:%_\+~#=]{{1,256}}\.[a-z]{{1,25}}[-a-zA-Z0-9@:%_\+.~#?&//=]",
        cast=True,
        flags=re.IGNORECASE,
        error_message=error_message,
    )


def email(require_tld: bool = True, *, error_message="Must be an email") -> InnerValidator:
    """Validates an email address

    There are very many ways to match email addresses, ranging from just requiring the ``@`` symbol, to a large and slow regex.

    This email validator is under development, and will, for the most part, validate valid email addresses: ie, no valid email address will be rejected. However, there are a great many strings that will still match, valid email or not.
    If you have your own method if validating email addresses, you can do that with a custom validator.

    Args:
        require_tld: Whether or not to require a TLD, like, ".com".

            Example: with ``require_tld=False``, ``meizuflux@example`` will be valid.
            With ``require_tld=True``, it will not be, but adding a ``.com`` will make it valid.
        error_message: The error message to raise if the value is not a valid email
    """
    to_compile = r"^(?=.{6,254}$)[0-9a-zA-Z_.+-]{1,249}@[0-9a-zA-Z_.-]{1,249}" + (
        r"\..{2,24}$" if require_tld else r"$"
    )
    return regex(to_compile, cast=False, flags=re.IGNORECASE, error_message=error_message)
