import cion
import pytest

from cion.exceptions import ValidationError
from cion.options import ExtraFields

def test_field():
    field = cion.Field()

    assert field.filters == []
    assert field.default == None
    assert field.nullable == False
    assert field.required == False

    with pytest.raises(ValueError):
        cion.Field(
            required=True,
            default="not none"
        )

def test_schema():
    options = cion.Options()

    schema = cion.Schema(
        fields={},
        options=options
    )

    assert schema.fields == {}
    assert schema.options == options

    with pytest.raises(ValueError):
        cion.Schema(
            fields={
                cion.schema.RESERVED_ERROR_KEY: cion.Field()
            }
        )

    del schema, options

    schema = cion.Schema(
        fields={
            "name": cion.Field(
                filters=[
                    cion.types.string()
                ],
                required=True,
                nullable=False
            ),
            "age": cion.Field(
                filters=[
                    cion.validators.range_(minimum=0, maximum=150)
                ],
                required=False,
                default=10
            ),
            "height": cion.Field()
        }
    )

    assert schema.validate({"name": "John"}) == {"name": "John", "age": 10}
    with pytest.raises(ValidationError):
        schema.validate({"name": None})

    with pytest.raises(ValidationError):
        schema.validate({})

    schema.validate({"name": "John", "age": "not an int"})

    with pytest.raises(ValidationError):
        schema.validate({"name": "John", "age": 151})

    schema.options.stop_on_error = True

    with pytest.raises(ValidationError):
        schema.validate({})

    schema.options.extra = ExtraFields.COMBINE

    assert schema.validate({"name": "John", "weight": 67}) == {"name": "John", "age": 10, "weight": 67}

    schema.options.extra = ExtraFields.ERROR

    with pytest.raises(ValidationError):
        schema.validate({"name": "John", "weight": 67})