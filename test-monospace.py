#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
from fontTools import ttLib

def main(filepaths):
    ERROR_OCCURRED = False

    # Begin report
    print("\nBegin test-monospace.py fixed width tests\n")

    try:
        expected_advance_width = int(sys.argv[-1])
    except Exception as e:
        sys.stderr.write("[test-monospace.py] ERROR: The last positional argument in the command is not the expected advance width integer value")

    filepaths_parsed = filepaths[0:-1]
    for fontpath in filepaths_parsed:
        if os.path.isfile(fontpath):
            print("\nTesting '" + fontpath + "'\n")
            tt = ttLib.TTFont(fontpath)

            # test for [post] table fixed pitch setting
            post_table_correct = tt['post'].__dict__['isFixedPitch']
            if post_table_correct == 0:
                sys.stderr.write("  X [post] table isFixedPitch setting is not correctly defined as 1.")

            # test for advance width settings in [hmtx] table
            hmtx_table = tt['hmtx'].__dict__['metrics']
            for glyph in hmtx_table:
                if hmtx_table[glyph][0] == expected_advance_width:
                    pass  # do nothing if it is the proper monospaced width
                else:
                    print(glyph + " : " + str(hmtx_table[glyph][0]))
        else:
            sys.stderr.write("[test-monospace.py] ERROR: The path '" + fontpath + "' does not appear to exist.")
            ERROR_OCCURRED = True


    if ERROR_OCCURRED == True:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    # call with python test-monospace.py [fontpath 1] <fontpath n...> [expected advance width]
    main(sys.argv[1:])
