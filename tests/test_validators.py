from contextlib import nullcontext
from uuid import UUID

import pytest

import cion
from cion import validators

RAISES = pytest.raises(cion.exceptions.ValidatorError)
DOES_NOT_RAISE = nullcontext()


@pytest.mark.parametrize(
    ("type_", "value", "expected_value", "expectation"),
    [
        (validators.length(), "1", "1", DOES_NOT_RAISE),
        (validators.length(maximum=3), "1000", "1000", RAISES),
        (validators.length(minimum=3), "1", "1", RAISES),
        (validators.length(minimum=3), [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], DOES_NOT_RAISE),
        (validators.length(maximum=1), [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1], RAISES),
        (validators.range_(minimum=3), 5, 5, DOES_NOT_RAISE),
        (validators.range_(maximum=3), 5, 5, RAISES),
        (validators.one_of("a"), "a", "a", DOES_NOT_RAISE),
        (validators.one_of("a"), "b", None, RAISES),
        (validators.not_one_of("a"), "b", "b", DOES_NOT_RAISE),
        (validators.not_one_of("a"), "a", None, RAISES),
        (validators.equal_to("a"), "a", "a", DOES_NOT_RAISE),
        (validators.equal_to("a"), "b", None, RAISES),
        (
            validators.uuid(),
            "9c10b73c-137f-4bc4-bf46-1f4ff29aac00",
            UUID("9c10b73c-137f-4bc4-bf46-1f4ff29aac00"),
            DOES_NOT_RAISE,
        ),
        (validators.uuid(), "1", None, RAISES),
        (validators.uuid(), "9c10b73c-137f-4bc4-bf46-1f4ff29aac0", None, RAISES),
        (validators.url(), "https://example.com", "https://example.com", DOES_NOT_RAISE),
        (validators.url(), "example.com", None, RAISES),
        (validators.url(["http"]), "https://example.com", None, RAISES),
        (validators.email(), "hello@meizuflux.com", "hello@meizuflux.com", DOES_NOT_RAISE),
        (validators.email(), "hello@meizuflux", None, RAISES),
        (validators.email(require_tld=False), "hello@meizuflux", "hello@meizuflux", DOES_NOT_RAISE),
    ],
)
def test_types(type_, value, expected_value, expectation):
    with expectation:
        assert type_(value) == expected_value
