#!/usr/bin/env python3
"""
Setup config for the utility package
"""

from setuptools import setup, find_packages

setup(
    name="cidc_utils",
    version='0.1.0',
    packages=find_packages(exclude=('tests', 'Pipfile', 'Pipfile.lock')),
    install_requires=[
        'amqp>=2.2.2',
        'kombu>=4.1.0',
        'requests>=2.18.4',
        'simplejson>=3.13.2',
        'sendgrid>=5.4.1',
        'bson==0.5.6'
    ],
    python_requires='>=3'
)
