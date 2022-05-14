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
    ("type_", "value", "expectation"),
    [
        (types.string, 1000, RAISES),
        (types.string, None, RAISES),
        (types.string, "1000", DOES_NOT_RAISE),
        (types.integer, 1000, DOES_NOT_RAISE),
        (types.integer, None, RAISES),
        (types.integer, "1000", RAISES),
    ],
)
def test_types(type_, value, expectation):
    with expectation:
        type_()(value)  # types return an inner function
