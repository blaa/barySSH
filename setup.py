#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name = "barySSH",
    version = "v0.2",
    author = "Tomasz Fortuna",
    author_email = "bla@thera.be",
    description = ("Proxy which uses simple time-based XOR scheme "
                   "to make heuristic detection of underlying "
                   "transmission impossible."),
    install_requires = ['twisted>=14.0.0'],
    license = "MIT",
    keywords = "ssh xor masking proxy tunnel",
    url = "https://github.com/blaa/barySSH",
    scripts=['baryssh'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
