#!/usr/bin/env python3
"""
Setup config for the utility package
"""

from setuptools import setup

setup(
    name="cidc_utils",
    version='0.1.0',
    packages=['caching', 'logging', 'requests'],
    python_requires='>=3'
)
