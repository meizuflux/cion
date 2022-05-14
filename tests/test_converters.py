from contextlib import nullcontext

import pytest

import cion
from cion import converters

RAISES = pytest.raises(cion.exceptions.ValidatorError)
DOES_NOT_RAISE = nullcontext()


class CannotCast:
    def __str__(self):
        return None


@pytest.mark.parametrize(
    ("type_", "value", "expected_value", "expectation"),
    [
        (converters.string, 1000, "1000", DOES_NOT_RAISE),
        (converters.string, None, "None", DOES_NOT_RAISE),
        (converters.string, "1000", "1000", DOES_NOT_RAISE),
        (converters.string, CannotCast(), None, RAISES),
        (converters.integer, 1000, 1000, DOES_NOT_RAISE),
        (converters.integer, None, None, RAISES),
        (converters.integer, "1000", 1000, DOES_NOT_RAISE),
    ],
)
def test_types(type_, value, expected_value, expectation):
    with expectation:
        assert type_()(value) == expected_value
