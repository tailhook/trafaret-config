#!/usr/bin/env python3

from setuptools import setup

setup(name='trafaret-config',
      version='0.1.0',
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
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      )
