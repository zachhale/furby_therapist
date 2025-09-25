#!/usr/bin/env python3
"""
Setup script for Furby Therapist CLI.
A whimsical therapeutic assistant that speaks in Furby language.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    """Read README.md for long description."""
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "A whimsical therapeutic assistant that speaks in Furby language"

# Read version from package
def get_version():
    """Get version from package."""
    version_file = os.path.join("furby_therapist", "__init__.py")
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return "1.0.0"

setup(
    name="furby-therapist",
    version=get_version(),
    author="Furby Therapist Team",
    author_email="furby@example.com",
    description="A whimsical therapeutic assistant that speaks in Furby language",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/furby-therapist/furby-therapist",
    project_urls={
        "Bug Reports": "https://github.com/furby-therapist/furby-therapist/issues",
        "Source": "https://github.com/furby-therapist/furby-therapist",
        "Documentation": "https://github.com/furby-therapist/furby-therapist/tree/main/docs",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Communications :: Chat",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    keywords="furby, therapy, cli, chatbot, therapeutic, assistant, mental-health, cycling",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "furby_therapist=furby_therapist.cli.main:main",
            "furby-therapist=furby_therapist.cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "furby_therapist": ["data/*.json", "data/*.md"],
    },
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "coverage>=5.0",
            "tox>=3.0",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "coverage>=5.0",
        ],
    },
    zip_safe=False,
)