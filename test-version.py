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
import re
import codecs
from fontTools import ttLib

def main(arguments):
    # Begin report
    print("\nBegin test-version.py font version tests...\n")

    ERROR_OCCURRED = False
    expected_version = arguments[-1]

    filepaths = arguments[0:-1]

    # regular expression match pattern for version string in fonts
    pattern = re.compile(r"Version\s(?P<version>\d\.\d{3})")

    for fontpath in filepaths:
        if os.path.isfile(fontpath):
            print("\n>>> Testing '" + fontpath + "'\n")
            tt = ttLib.TTFont(fontpath)

            version_string_raw = ""
            name_tables = tt['name'].__dict__['names']
            for name_table in name_tables:
                if name_table.__dict__['nameID'] == 5 and name_table.__dict__['platformID'] == 1:
                    osx_version_string_raw = name_table.__dict__['string']
                elif name_table.__dict__['nameID'] == 5 and name_table.__dict__['platformID'] == 3:
                    win_version_string_raw = name_table.__dict__['string']

            # nameID = 5, platformID = 1 (OS X)
            if len(osx_version_string_raw) > 0:
                if type(osx_version_string_raw) == bytes:
                    osx_version_string_raw = bytes.decode(osx_version_string_raw, "utf-8")
                if osx_version_string_raw.startswith("Version"):
                    m = pattern.search(osx_version_string_raw)
                    osx_observed_version = m.group('version')
                    if osx_observed_version == expected_version:
                        print("[test-version.py] Expected version string '" + expected_version + "' was detected in the name tables for nameID=5, platformID=1.\n\n")
                    else:
                        sys.stderr.write("[test-version.py] ERROR: Expected version '" + expected_version + "' does not equal observed version '" + osx_observed_version + "' for nameID=5, platformID=1\n\n")
                        ERROR_OCCURRED = True
                else:
                    sys.stderr.write("[test-version.py] ERROR: Did not detect 'Version X.XXX' syntax at the beginning of the version string in nameID=5, platformID=1 name table.\n\n")
                    ERROR_OCCURRED = True
            else:
                sys.stderr.write("[test-version.py] ERROR: unable to parse the version string from the nameID = 5, platformID=1 table for '" + fontpath + "'.\n\n")
                ERROR_OCCURRED = True

            # nameID = 5, platformID = 3 (Windows)
            if len(win_version_string_raw) > 0:
                # UTF-16 big endian encoded table string in Windows name tables, need to convert
                win_version_string_decoded = bytes.decode(win_version_string_raw, "utf-16-be")
                if win_version_string_decoded.startswith("Version"):
                    m = pattern.search(win_version_string_decoded)
                    win_observed_version = m.group('version')
                    if win_observed_version == expected_version:
                        print("[test-version.py] Expected version string '" + expected_version + "' was detected in the name tables for nameID=5, platformID=3.\n\n")
                    else:
                        sys.stderr.write("[test-version.py] ERROR: Expected version '" + expected_version + "' does not equal observed version '" + win_observed_version + "' for nameID=5, platformID=3\n\n")
                        ERROR_OCCURRED = True
                else:
                    sys.stderr.write("[test-version.py] ERROR: Did not detect 'Version X.XXX' syntax at the beginning of the version string in nameID=5, platformID=3 name table.\n\n")
                    ERROR_OCCURRED = True
            else:
                sys.stderr.write("[test-version.py] ERROR: unable to parse the version string from the nameID = 5, platformID=3 table for '" + fontpath + "'.\n\n")
                ERROR_OCCURRED = True

    if ERROR_OCCURRED is True:
        sys.exit(1)
    else:
        sys.exit(0)



if __name__ == '__main__':
    # call with python test-version.py [fontpath 1] <fontpath n...> [expected version in X.XXX format]
    main(sys.argv[1:])
