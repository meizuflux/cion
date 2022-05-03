build:
    rm -rf build dist *.egg-info
    python -m build

upload:
    twine upload dist/*