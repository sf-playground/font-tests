#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  ------------------------------------------------------------------------------
#  test-monospace.py
#  Copyright 2015 Christopher Simpkins
#  MIT license
#  ------------------------------------------------------------------------------

import sys
import os
import os.path
from fontTools import ttLib

def main(filepaths):
    ERROR_OCCURRED = False

    # Begin report
    print("\nBegin test-monospace.py fixed width tests...\n")

    try:
        expected_advance_width = int(sys.argv[-1])
    except Exception as e:
        sys.stderr.write("[test-monospace.py] ERROR: The last positional argument in the command is not the expected advance width integer value\n")

    filepaths_parsed = filepaths[0:-1]
    for fontpath in filepaths_parsed:
        if os.path.isfile(fontpath):
            print("\n>>> Testing '" + fontpath + "'\n")
            tt = ttLib.TTFont(fontpath)

            # test for [post] table fixed pitch setting
            post_table_correct = tt['post'].__dict__['isFixedPitch']
            if post_table_correct == 0:
                sys.stderr.write("[test-monospace.py] ERROR: [post] table isFixedPitch setting is not defined as 1.\n")
                ERROR_OCCURRED = True

            # test for advance width settings in [hmtx] table
            hmtx_table = tt['hmtx'].__dict__['metrics']
            incorrect_width_dict = {}
            for glyph in hmtx_table:
                if hmtx_table[glyph][0] == expected_advance_width:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                else:
                    incorrect_width_dict[glyph] = str(hmtx_table[glyph][0])
                    sys.stdout.write("X")
                    sys.stdout.flush()
                    ERROR_OCCURRED = True
        else:
            sys.stderr.write("[test-monospace.py] ERROR: The path '" + fontpath + "' does not appear to exist.\n")
            ERROR_OCCURRED = True

        if len(incorrect_width_dict) > 0:
            sys.stderr.write("\n\n[test-monospace.py] ERROR: The following glyphs in the font '" + fontpath + "' have an advance width that failed to match your expected metric of " + str(expected_advance_width) + " units:\n")
            for x in incorrect_width_dict.keys():
                sys.stderr.write("  " + x + " : " + str(incorrect_width_dict[x]) + "\n")

    if ERROR_OCCURRED == True:
        sys.exit(1)  # exit with status code 1
    else:
        print("[test-monospace.py] Tests complete. All tests passed.\n")
        sys.exit(0)  # exit with status code 0


if __name__ == '__main__':
    # call with python test-monospace.py [fontpath 1] <fontpath n...> [expected advance width]
    main(sys.argv[1:])
