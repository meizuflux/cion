from typing import Callable, Any, Iterable
from cion.exceptions import ValidatorError

Validator = Callable[[Any], Any]

def length(minimum: int, maximum: int, error_message: str = "Length must be between {minimum} and {maximum}") -> Validator:
    def inner(value: str):
        if len(value) < minimum or len(value) > maximum:
            raise ValidatorError(error_message.format(minimum=minimum, maximum=maximum))
        return value
    return inner

def one_of(values: Iterable[Any], error_message: str = "Value must be one of {values}"):
    def inner(value: Any):
        if value not in values:
            raise ValidatorError(error_message.format(values=", ".join(str(v) for v in values)))
        return value
    return inner