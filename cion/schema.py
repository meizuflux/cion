"""Objects for defining schema to validate data"""
from collections import defaultdict
from typing import Any, Callable, Optional

from cion.exceptions import ValidationError, ValidatorError
from cion.options import ExtraFieldsOption, Options

__all__ = (
    "Field",
    "Schema",
)

Validator = Callable[[Any], Any]

RESERVED_ERROR_KEY = "__schema__"


class Field:
    """A field in a Schema"""

    validators: list[Validator]
    default: Optional[Any] = None
    allow_none: bool
    required: bool = False

    def __init__(
        self,
        *,
        type_: Validator,
        validators: Optional[list[Validator]] = None,
        default: Any = None,
        allow_none: bool = False,
        required: bool = False,
    ) -> None:
        """Create a field for use in a Schema

        data is assumed to be the data passed to :meth:`Schema.validate_data`

        Args:
            type_: The type of the field.
                This is the first validator that gets called
            validators: A list of validators.
                The validators are called in the exact order that they are specified, so when using multiple, ensure that it is the exact way that you want it
            default: The default value for the field, if it is not present in the data
            allow_none: Whether to allow the value for the field to be None or not.
                When this is ``True`` and the value is None, no validators are called
            required: Whether or not the field is required to be in the data

        """
        if validators is None:
            validators = []

        validators.append(type_)

        self.validators = validators
        self.default = default
        self.allow_none = allow_none
        self.required = required


class Schema:
    """Schema to validate data"""

    fields: dict[str, Field]
    options: Options

    def __init__(self, fields: dict[str, Field], options: Optional[Options] = None) -> None:
        """Create schema instance

        Initializes a schema instance that can be used to validate data

        Args:
            fields: A dictionary of fields, with the keys being names and the values being an instance of :class:`cion.Field`
            options: Optional options to add extra functionality to the schema

        Notes:
            ``__schema__`` is not allowed to be a field name, it is reserved for internal usage

        Raises:
            ValueError: If ``__schema__`` is included as a field name

        """
        if RESERVED_ERROR_KEY in fields:
            raise ValueError(f"{RESERVED_ERROR_KEY} cannot be a field name, for it is reserved for internal purposes")

        self.fields = fields
        self.options = options or Options()

    def validate(self, data: dict[Any, Any]) -> dict[Any, Any]:
        """Validate a dict according to the defined schema

        Goes through every item in the data and applies constraints to it

        Note:
            It is important to ensure that ``data`` is an iterable that can have data removed.
            It is highly reccomended to convert it to a dict before calling this method.

        Args:
            data: The data to be validated

        Returns
            The validated and transformed data depending on the specified validators

        Raises:
            ValidationError: When ``self.stop_on_error`` is true and a field in the data does not validate properly
            ValidationError: When ``self.stop_on_error`` is false, this will contain all the errors, if any
        """
        errors = defaultdict(list)
        validated: dict[str, Any] = {}

        def raise_error(field_name: str, error_message: str, *, delete_field: bool = True):
            if delete_field is True:
                del data[field_name]
            if self.options.stop_on_error is True:
                raise ValidationError({field_name: [error_message]}, {})
            errors[name].append(error_message)

        for name, options in self.fields.items():
            # We can't use dict.get since the value may be allowed to be None
            try:
                value = data[name]
            except KeyError:
                if options.required is True and options.default is None:
                    raise_error(name, "This field is required", delete_field=False)
                    continue
                if options.default is not None:
                    value = options.default
                else:
                    continue

            if value is None:
                if options.allow_none is not True:
                    raise_error(name, "This field is not allowed to be None")
                    continue

            for validator in options.validators:
                if value is not None:
                    try:
                        value = validator(value)
                    except ValidatorError as error:
                        raise_error(name, error.message)
                        continue

            validated[name] = value

        # We don't need to account for ExtraFields.IGNORE
        # since IGNORE means don't do anything

        # Since the validated data is deleted from the original data
        # anything left over is extra
        if self.options.extra is ExtraFieldsOption.COMBINE:
            validated = validated | data

        if self.options.extra is ExtraFieldsOption.ERROR:
            raise_error(RESERVED_ERROR_KEY, f"Found extra data: {', '.join(data.keys())}", delete_field=False)

        if bool(errors):  # Checks if there are any keys
            raise ValidationError(errors, validated)

        return validated
