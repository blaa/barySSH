#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from setuptools.extension import Extension

try:
    from Cython.Build import cythonize
    USE_CYTHON=True
except ImportError:
    print
    print
    print "You need Cython to compile this project"
    print
    raise
    USE_CYTHON=False
    cythonize = lambda x: x
    print "Trying to work without cython"

ext = '.pyx' if USE_CYTHON else '.c'

setup(
    name = "barySSH",
    version = "v0.3.3",
    author = "Tomasz Fortuna",
    author_email = "bla@thera.be",
    description = ("Proxy which uses simple time-based XOR scheme "
                   "to make heuristic detection of underlying "
                   "transmission impossible."),
    install_requires = ['twisted>=14.0.0', 'cython>=0.21.1'],
    license = "MIT",
    keywords = "ssh xor masking proxy tunnel",
    url = "https://github.com/blaa/barySSH",
    scripts=['baryssh'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    ext_modules = cythonize(
        Extension(
            "barylib",
            ["barylib/*.pyx"],
        )
    )
)
