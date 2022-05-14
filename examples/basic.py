import sys

sys.path.insert(0, "..")


from cion import Field, Schema, types, validators

User = Schema(
    fields={
        "username": Field(
            filters=[
                types.string(),
                validators.length(3, 64),
            ],
            required=False,
            default="testing1234",
        ),
        "password": Field(
            filters=[types.string(), validators.length(8, 1024)],
            required=True,
        ),
    },
)


data = {
    "username": 12312312,
    "password": "password",
}

print(User.validate(data))
