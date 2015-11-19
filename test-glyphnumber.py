#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  ------------------------------------------------------------------------------
#  test-glyphnumber.py
#  Copyright 2015 Christopher Simpkins
#  MIT license
#  ------------------------------------------------------------------------------

import sys
import os
import os.path
from fontTools import ttLib

def main(arguments):
    # Begin report
    print("\nBegin test-glyphnumber.py glyph number tests...\n")

    ERROR_OCCURRED = False

    try:
        expected_glyph_no = int(arguments[-1])
    except Exception as e:
        sys.stderr.write("[test-glyphnumber.py] ERROR: the last positional argument should be an integer to define the expected number of glyphs.\n")
        sys.exit(1)

    filepaths = arguments[0:-1]

    for fontpath in filepaths:
        if os.path.isfile(fontpath):
            print("\n>>> Testing '" + fontpath + "'\n")
            tt = ttLib.TTFont(fontpath)

            # test glyph number from [maxp] table
            observed_glyph_no = tt['maxp'].__dict__['numGlyphs']
            if observed_glyph_no == expected_glyph_no:
                print("  ✓ " + fontpath + " glyph number is " + str(expected_glyph_no))
            else:
                sys.stderr.write("  X " + fontpath + " glyph number is " + str(observed_glyph_no) + " NOT " + str(expected_glyph_no))
                ERROR_OCCURRED = True
        else:
            sys.stderr.write("[test-glyphnumber.py] ERROR: The path '" + fontpath + "' is not a path to a font file.\n")
            sys.exit(1)


    if ERROR_OCCURRED is True:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    # call with python test-glyphnumber.py [fontpath 1] <fontpath n...> [expected number]
    main(sys.argv[1:])
