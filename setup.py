#!/usr/bin/env python
# encoding: utf-8
from distutils.core import setup
import os.path
import sys

if sys.platform == 'darwin':
    ## tell OS X tar not to include resource forks
    os.environ['COPYFILE_DISABLE'] = '1'

readme_text = file(os.path.join(os.path.dirname(__file__), 'README')).read()

setup(name='Factory',
      version='1.2',
      description='Object Oriented Currying',
      long_description=readme_text,
      author='Peter Fein',
      author_email='pfein@pobox.com',
      url='http://code.google.com/p/python-factory/',
      py_modules=['Factory'],

     )