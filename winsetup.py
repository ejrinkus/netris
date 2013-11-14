################################################################################
#
#  Script for building an executable on Windows
#
################################################################################

__author__ = 'Eric'

from distutils.core import setup
import py2exe

setup(console=['netris.py'])
