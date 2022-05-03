from setuptools import setup
import re

with open("neptune/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open("README.md") as f:
    readme = f.read()

setup(
    name="neptune",
    description="A data validation library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="meizuflux",
    license="MIT",
    url="https://github.com/meizuflux/neptune",
    packages=["neptune", "neptune.contrib"],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    version=version,
    install_requires=[],
    python_requires=">=3.10.2"
)