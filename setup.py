#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
        name='subfind',
        version='0.1.0.5',
        description='Subtitle crawler written in Python',
        author='Thong Dong',
        author_email='thongdong7@gmail.com',
        url='https://github.com/thongdong7/pysub',
        packages=find_packages(exclude=["build", "dist", "tests*"]),
        install_requires=['lxml', 'Distance==0.1.3', 'clint'],
        entry_points={
            'console_scripts': [
                'subfind = pysub.cli:main',
            ],
        },
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Environment :: Console",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
        ],
)
