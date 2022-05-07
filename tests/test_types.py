from contextlib import nullcontext

import pytest

import cion
from cion import types

RAISES = pytest.raises(cion.exceptions.ValidatorError)
DOES_NOT_RAISE = nullcontext()


class CannotCast:
    def __str__(self):
        return None


@pytest.mark.parametrize(
    ("type_", "cast", "value", "expected_value", "expectation"),
    [
        (types.string, True, 1000, "1000", DOES_NOT_RAISE),
        (types.string, True, CannotCast(), None, RAISES),
        (types.string, False, 1000, 1000, RAISES),
        (types.string, False, CannotCast(), None, RAISES),
        (types.integer, True, "1000", 1000, DOES_NOT_RAISE),
        (types.integer, True, "1000.0", 1000, RAISES),
        (types.integer, True, "not an integer", None, RAISES),
        (types.integer, False, 1000, 1000, DOES_NOT_RAISE),
        (types.integer, False, "1000", 1000, RAISES),
        (types.integer, False, "not an integer", 1000, RAISES),
    ],
)
def test_cast_type(type_, cast, value, expected_value, expectation):
    with expectation:
        assert type_(cast=cast)(value) == expected_value
