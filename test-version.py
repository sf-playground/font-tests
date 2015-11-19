#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  ------------------------------------------------------------------------------
#  test-version.py
#  Copyright 2015 Christopher Simpkins
#  MIT license
#  ------------------------------------------------------------------------------

import sys
import os
import os.path
from fontTools import ttLib

def main(arguments):
    pass


if __name__ == '__main__':
    # call with python test-version.py [fontpath 1] <fontpath n...> [expected version in X.XXX format]
    main(sys.argv[1:])
