import sys

sys.path.insert(0, "../..")

from aiohttp import web

import cion

LoginSchema = cion.Schema(
    fields={
        "username": cion.Field(
            filters=[cion.types.string(), cion.validators.length(3, 64)],
            required=True,
        ),
        "password": cion.Field(
            filters=[cion.types.string(), cion.validators.length(3, 1024)],
            required=True,
        ),
    }
)

FORM = """
<!DOCTYPE html>
<html>
<body>
    <form action="/validate_data" method="POST">
        <input type="text" name="username" placeholder="username">
        <input type="password" name="password" placeholder="password">
        <button type="submit">submit</button>
        <br>
        {errors}
    </form>
</body>
</html>
"""

FORM_SUBMIT = """
<!DOCTYPE html>
<html>
<body>
    <pre>
Username: {username}
Password: {password}
    </pre>
</body>
</html>
"""


def index(_: web.Request):
    return web.Response(body=FORM.format(errors="").encode("utf-8"), content_type="text/html")


async def validate_data(request: web.Request):
    data = await request.post()

    try:
        validated_data = LoginSchema.validate(dict(data))
    except cion.ValidationError as error:
        return web.Response(
            body=FORM.format(errors="<br>".join(f"{k}: {', '.join(v)}" for k, v in error.errors.items())).encode(
                "utf-8"
            ),
            content_type="text/html",
        )

    return web.Response(
        body=FORM_SUBMIT.format(username=validated_data["username"], password=validated_data["password"]).encode(
            "utf-8"
        ),
        content_type="text/html",
    )


def create_app():
    app = web.Application()
    app.add_routes([web.get("/", index), web.post("/validate_data", validate_data)])

    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="localhost", port=8080)
