build:
    rm -rf build dist *.egg-info
    python setup.py bdist_wheel

upload:
    twine upload dist/*