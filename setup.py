import re

from setuptools import find_packages, setup

version = None
with open("cion/__init__.py") as f:
    for line in f.read().splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
if version is None:
    raise RuntimeError("Unable to find version string.")

with open("README.rst") as f:
    readme = f.read()

setup(
    name="cion",
    description="A data validation library",
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="meizuflux",
    project_urls={
        "Documentation": "https://cionpy.readthedocs.io",
        "Issue Tracker": "https://github.com/meizuflux/cion/issues",
        "Source Code": "https://github.com/meizuflux/cion",
    },
    license="MIT",
    url="https://github.com/meizuflux/cion",
    packages=find_packages(),
    package_data={"cion": ["py.typed"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    version=version,
    install_requires=[],
    extras_require={
        "docs": [
            "sphinx",
            "sphinx-copybutton",
            "sphinx-autobuild",
        ],
        "lint": [
            "pyright",
        ],
        "build": [
            "setuptools",
            "wheel",
            "build",
            "twine",
        ],
        "format": [
            "black",
            "isort",
        ],
        "test": [
            "pytest",
            "coverage[toml]",
            "pytest-cov",
        ],
    },
    python_requires=">=3.10",
)
