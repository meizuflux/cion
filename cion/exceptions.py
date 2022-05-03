from typing import Any, Optional

class CionException(Exception):
    ...

class ValidatorError(CionException):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message

Errors = dict[str, list[str]]
ValidData = dict[str, Any]

class ValidationError(CionException):
    errors: Errors
    data: Optional[ValidData] = None

    def __init__(self, errors: Errors, valid_data: ValidData) -> None:
        self.errors = errors
        self.data = valid_data
        super().__init__("Errors were raised: " + str(dict(self.errors)))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} errors={self.errors} data={self.data}>"