import csv
from contextlib import nullcontext

import pytest

import cion
from cion import types

RAISES = pytest.raises(cion.exceptions.ValidatorError)
DOES_NOT_RAISE = nullcontext()

emails = []
with open("tests/email/emails") as f:
    for line in f.readlines():
        if line.startswith("#") or line.startswith("\n"):
            continue
        email_test = line.split(",")
        raises = RAISES if email_test[1] == "true" else DOES_NOT_RAISE
        emails.append((email_test[0], raises, bool(email_test[2])))


@pytest.mark.parametrize(
    ("email", "expectation", "require_tld"),
    emails,
)
def test_email(email, expectation, require_tld):
    with expectation:
        cion.validators.email(require_tld=require_tld)(email)
