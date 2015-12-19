#!/usr/bin/env python

from setuptools import setup

setup(
        name='pysub',
        version='0.1.0.0',
        description='Subtitle crawler written in Python',
        author='Thong Dong',
        author_email='thongdong7@gmail.com',
        install_requires=['lxml', 'clint'],
        entry_points={
            'console_scripts': [
                'subfind = pysub.cli:main',
            ],
        }
)
