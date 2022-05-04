from typing import Any, Optional

__all__ = ("CionException", "ValidatorError", "ValidationError")


class CionException(Exception):
    """Base class for all exceptions raised by Cion"""


class ValidatorError(CionException):
    """Exception raised by a validator"""

    message: str  #: The message that the validator raised

    def __init__(self, message: str) -> None:
        self.message = message


Errors = dict[str, list[str]]
ValidData = dict[str, Any]


class ValidationError(CionException):
    """Error raised when validating data"""

    errors: Errors  #: A dictionary containing all of the errors
    data: Optional[ValidData] = None  #: Contains all of the validated data

    def __init__(self, errors: Errors, valid_data: ValidData) -> None:
        self.errors = errors
        self.data = valid_data
        super().__init__("Errors were raised: " + str(dict(self.errors)))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} errors={self.errors} data={self.data}>"
