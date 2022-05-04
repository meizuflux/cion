"""Schema Options"""
from enum import Enum

__all__ = ("Options", "ExtraFieldsOption")


class ExtraFieldsOption(Enum):
    """Enum that dictates what to do in the event that there is extra data"""

    IGNORE = "ignore"  #: Ignore the extra data and only return the validated data
    COMBINE = "combine"  #: Combine the extra fields and the validated data
    ERROR = "error"  #: Return a :class:`cion.exceptions.ValidationError` with a list of the unexpected fields


class Options:
    """Schema Options"""

    extra: ExtraFieldsOption = ExtraFieldsOption.IGNORE
    stop_on_error: bool = False

    def __init__(
        self,
        *,
        extra: ExtraFieldsOption = ExtraFieldsOption.IGNORE,
        stop_on_error: bool = False,
    ) -> None:
        """Class for creating Schema options

        Args:
            extra: What to do when there are extra fields in the data

                See the docs for :class:``cion.options.ExtraFieldsOption``
            stop_on_error: Whether or not to continue after an error
                If ``True``, when an error is raised, stop immediately and throw an error

                If ``False``, when an error is raised, compile a list of errors and throw the error after validation is done

                Essentially, this option dictates whether you want to receive any validated data on error, or wait to get all the valid data
        """
        self.extra = extra
        self.stop_on_error = stop_on_error
