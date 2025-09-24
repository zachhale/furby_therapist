#!/usr/bin/env python3
"""
Setup script for Furby Therapist CLI.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="furby-therapist",
    version="1.0.0",
    author="Furby Therapist Team",
    description="A whimsical therapeutic assistant that speaks in Furby language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "furby_therapist=furby_therapist.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "furby_therapist": ["*.json", "*.md"],
    },
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ],
    },
)