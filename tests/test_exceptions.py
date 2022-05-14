import cion

def test_validation_error():
    error = cion.ValidationError(
        {"username": ["Must be a string"]},
        {"password": "qwertyuiop"}
    )

    assert error.errors == {"username": ["Must be a string"]}
    assert error.data == {"password": "qwertyuiop"}

    assert str(error) == "Errors were raised: {'username': ['Must be a string']}"

    assert f"{error!r}" == "<ValidationError errors={'username': ['Must be a string']} data={'password': 'qwertyuiop'}>"