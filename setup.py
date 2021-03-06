#!/usr/bin/env python


import distutils
from distutils.core import setup, Extension

setup(
    name = 'larch',
    version = '0.9.4',
    author = 'Matthew Newville',
    author_email = 'newville@cars.uchicago.edu',
    license = 'Python',
    description = 'A data processing macro language for python',
    packages = ['larch','larch.plugins','larch.modules',
                'larch.wxlarch', 'larch.wxlarch.mplot'],
    package_data = {'larch.modules':['startup.lar']},
    data_files  = [('bin',['bin/larch', 'bin/wxlarch'])],)

