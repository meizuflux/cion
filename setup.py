import re

from setuptools import find_packages, setup

with open("cion/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open("README.md") as f:
    readme = f.read()

setup(
    name="cion",
    description="A data validation library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="meizuflux",
    project_urls={
        "Documentation": "https://cionpy.readthedocs.io",
        "Issue Tracker": "https://github.com/meizuflux/cion/issues",
        "Source Code": "https://github.com/meizuflux/cion",
    },
    license="MIT",
    url="https://github.com/meizuflux/cion",
    packages=find_packages(),
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
        "docs": ["sphinx", "furo", "sphinx-copybutton"],
        "lint": [
            "pyright",
        ],
        "build": ["setuptools", "wheel", "build"],
        "format": ["black", "isort"],
    },
    python_requires=">=3.10",
)
