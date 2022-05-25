build:
    rm -rf build dist *.egg-info
    python -m build

upload:
    twine upload dist/*

build-docs:
    sphinx-build -a -n -N --keep-going -T -j auto docs docs/_build/html

dev:
    sphinx-autobuild -a -n -N -T -j auto docs docs/_build/html

serve +PORT="8000":
    python -m http.server {{PORT}} --directory docs/_build/html --bind 127.0.1

install:
    pip install -e ".[docs,lint,build,format,test]"

lint:
    pyright

test:
    pytest --cov-report term --cov-report xml:coverage.xml --cov=cion tests/

format:
    black .
    isort .

prebuild: build-docs && format lint test