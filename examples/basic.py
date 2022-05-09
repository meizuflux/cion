import sys

sys.path.insert(0, "..")


from cion import Field, Schema, types, validators

User = Schema(
    fields={
        "username": Field(
            type_=types.string(),
            validators=[validators.length(3, 64)],
            default="testing1234",
        ),
        "password": Field(
            type_=types.string(),
            validators=[validators.length(8, 1024)],
            required=True,
        ),
    },
)


data = {
    "username": "meizuflux",
    "password": "password",
}

print(User.validate(data))
