#!/usr/bin/env python

# This file is generated by `code-gen`. Any change in this file could be override

from setuptools import setup, find_packages

setup(
    name='subfind',
    version='4.6.0',
    description='Subtitle crawler written in Python',
    author='Thong Dong',
    author_email='thongdong7@gmail.com',
    url='https://github.com/thongdong7/subfind',
    packages=find_packages(exclude=["test*"]),
    install_requires=[
        'six==1.10.0',
    ],
    extras_require={
        'cli': ['click==6.6', 'pyyaml==3.11', 'requests==2.9.1', 'babelfish==0.5.5', 'beautifulsoup4==4.4.1'],
        'opensubtitles': ['requests==2.9.1', 'babelfish==0.5.5'],
        'subscene': ['requests==2.9.1', 'beautifulsoup4==4.4.1'],
        'web': ['flask==0.10.1', 'tornado==4.3', 'click==6.6', 'gevent==1.2.2'],
    },
    entry_points={
        'console_scripts': [
            'subfind-web=subfind_web.script:run',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: Python Software Foundation License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        # "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    include_package_data=True,
)