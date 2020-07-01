#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from typing import List

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

setup_requirements = ["pytest-runner"]  # type: List[str]

test_requirements = ["pytest"]  # type: List[str]

setup(
    author="Jori Geysen",
    author_email="jori.geysen@anmut.co.uk",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    dependency_links=[],
    description="Extracting relevant parts of text from a larger body of text. Given a term, this repo creates the tools necessary to determine how relevant a part of text is to that term; the output of which can be used to filter irrelevant sentences.",
    install_requires=["pandas", "numpy", "spacy", "nltk"],
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="relevance",
    name="relevance",
    packages=find_packages(include=["relevance*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jgeysen-work/relevance",
    version="0.0.1",
    zip_safe=False,
)
