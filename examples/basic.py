from cion import Schema, validators, types

class User(Schema):
    fields = {
        "username": {
            "type": types.string(),
            "constraints": [
                validators.length(3, 64),
            ],
            "required": True
        },
        "password": {
            "type": types.string(),
            "constraints": [
                validators.length(3, 1024)
            ],
            "required": True
        },
        "role": {
            "type": types.string(),
            "constraints": [
                validators.one_of({"admin", "user"})
            ],
            "required": False
        }
    }

data = {
    "username": "meizuflux",
    "password": "password",
    "role": "admin"
}

inst = User(data)

print(inst.validate())



