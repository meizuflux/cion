from cion.exceptions import ValidatorError

def string(cast: bool = True):
    def inner(value: str):
        if not isinstance(value, str):
            if cast:
                value = str(value)
            else:
                raise ValidatorError("Field must be a valid string")
        return value
    return inner

def integer(cast: bool = False):
    def inner(value: int):
        if not isinstance(value, int):
            if cast:
                value = int(value)
            else:
                raise ValidatorError("Field must be a valid integer")
        return value
    return inner