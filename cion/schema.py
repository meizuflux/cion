from collections import defaultdict

from cion import types
from cion.exceptions import ValidationError, ValidatorError


class Schema:
    """Class that defines schema for data"""

    fields: dict[str, dict]  #: The fields to be validated
    ignore_extra: bool = False  #: Whether or not to ignore extra keys in the data

    def __init__(self, data: dict, ignore_extra: bool = False) -> None:
        for value in self.fields.values():
            value.setdefault("type", types.string())
            value.setdefault("constraints", [])

            value["constraints"].insert(0, value["type"])

        self.__data = data
        self.ignore_extra = ignore_extra

    def validate(self):
        """Validates the data

        Runs through all of the data and checks it against the fields

        Raises:
            ValidationError: When there is an error when validating
            ValueError: When ``self.ignore_extra`` is `False`, and there are extra values in the data
        """
        errors = defaultdict(list)
        valid_data = {}

        for key, value in self.__data.items():
            field = self.fields.get(key)
            if field is None and self.ignore_extra is False:
                raise ValueError(f"Unexpected field with name {key} found")
            errored = False
            for validator in field["constraints"]:
                try:
                    value = validator(value)
                except ValidatorError as error:
                    errored = True
                    errors[key].append(error.message)
            if errored is False:
                valid_data[key] = value

        for key, field in self.fields.items():
            value = valid_data.get(key)
            if value is None:
                if field.get("default") is not None:
                    valid_data[key] = field.get("default")
                elif field.get("required") is True:
                    errors[key].append(["This field is required"])

        try:
            valid_data = self.after_load(valid_data)
        except NotImplementedError:
            pass

        if bool(errors):  # check if empty basically, returns true if filled
            raise ValidationError(errors, valid_data)

        return valid_data

    def after_load(self, data: dict):
        """Function called after data is validated

        The default implementation is to raise NotImplementedError

        Args:
            data (dict): The validated data

        """
        raise NotImplementedError()
