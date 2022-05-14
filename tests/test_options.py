import cion


def test_options():
    options = cion.Options(extra=cion.options.ExtraFields.COMBINE, stop_on_error=False)

    assert options.extra == cion.options.ExtraFields.COMBINE
    assert options.stop_on_error == False
