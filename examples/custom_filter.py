import sys
from typing import Iterable

sys.path.insert(0, "../..")

import cion


def numbers_in_order(value: list[int]):
    if not isinstance(value, Iterable):
        raise cion.exceptions.ValidatorError("Must be a list of ints")

    for i in enumerate(value):
        item = value[i]

        if not isinstance(item, int):
            raise cion.exceptions.ValidatorError("Must be a list of ints")

        if i != 0:
            if item < value[i - 1]:
                raise cion.exceptions.ValidatorError("Items must be in order")

    return value


# [Schema Start]
schema = cion.Schema(
    fields={
        "code": cion.Field(
            filters=[numbers_in_order],
            required=True,
        )
    }
)
# [Schema End]

# [Start OK]
print(schema.validate({"code": [1, 2, 3, 4, 5]}))
# [End OK]

# [Start Fails: list]
try:
    schema.validate({"code": "cion"})
except cion.ValidationError as error:
    print(error)
# [End Fails: list]

# [Start Fails: int]
try:
    schema.validate({"code": ["cion"]})
except cion.ValidationError as error:
    print(error)
# [End Fails: int]

# [Start Fails: order]
try:
    schema.validate({"code": [5, 4, 3, 2, 1]})
except cion.ValidationError as error:
    print(error)
# [End Fails: order]
