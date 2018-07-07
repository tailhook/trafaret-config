#!/usr/bin/env python3

from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), 'rt') as f:
    long_description = f.read()

setup(name='trafaret-config',
      version='2.0.1b2',
      description='A configuration library for python using trafaret and yaml',
      author='Paul Colomiets',
      author_email='paul@colomiets.name',
      url='http://github.com/tailhook/trafaret-config',
      packages=['trafaret_config'],
      install_requires=[
        'PyYaml',
        'trafaret',
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'License :: OSI Approved :: MIT License',
          'License :: OSI Approved :: Apache Software License',
      ],
      long_description=long_description,
)
