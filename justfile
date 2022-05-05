build:
    rm -rf build dist *.egg-info
    python -m build

upload:
    twine upload dist/*

build-docs:
    sphinx-build -a -n -N --keep-going -T -j auto docs docs/_build/html

serve +PORT="8000":
    python -m http.server {{PORT}} --directory docs/_build/html

install:
    pip install -e ".[docs,lint,build,format]"

lint:
    pyright

format:
    black .
    isort .