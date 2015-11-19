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
    # Begin report
    print("\nBegin test-version.py font version tests...\n")

    ERROR_OCCURRED = False
    expected_version = arguments[-1]

    filepaths = arguments[0:-1]

    for fontpath in filepaths:
        if os.path.isfile(fontpath):
            print("\n>>> Testing '" + fontpath + "'\n")
            tt = ttLib.TTFont(fontpath)

            version_string_raw = ""
            name_tables = tt['name'].__dict__['names']
            for name_table in name_tables:
                if name_table.__dict__['nameID'] == 5:
                    version_string_raw = name_table.__dict__['string']

            if len(version_string_raw) > 0:
                pass
                # TODO: parse the version number from the raw version string and compare
            else:
                sys.stderr.write("[test-version.py] ERROR: unable to parse the version string from the nameID = 5 table for '" + fontpath + "'.")
                ERROR_OCCURRED = True

    if ERROR_OCCURRED is True:
        sys.exit(1)
    else:
        sys.exit(0)



if __name__ == '__main__':
    # call with python test-version.py [fontpath 1] <fontpath n...> [expected version in X.XXX format]
    main(sys.argv[1:])
