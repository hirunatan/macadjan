# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import os, sys

try:
    from .local import *
except ImportError:
    print(u"«local.py» file does not exist.")
    print(u"Go to settings directory and copy «local.py.example» to «local.py»")
    sys.exit(-1)

