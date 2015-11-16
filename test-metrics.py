#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import hashlib
from fontTools import ttLib

from yaml import load, dump
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class MetricsObject(object):
    def __init__(self, fontpath):
        unitsPerEm = 0              # [head] unitsPerEm
        ascent = 0                  # [hhea] ascent
        descent = 0                 # [hhea] descent
        lineGap = 0                 # [hhea] lineGap
        capheight = 0               # [OS/2] sCapHeight
        xheight = 0                 # [OS/2] sxHeight
        typoAscender = 0            # [OS/2] sTypoAscender
        typoDescender = 0           # [OS/2] sTypoDescender
        typoLineGap = 0             # [OS/2] sTypoLineGap
        winAscent = 0               # [OS/2] usWinDescent
        winDescent = 0              # [OS/2] usWinAscent
        strikeoutPosition = 0       # [OS/2] yStrikeoutPosition
        strikeoutSize = 0           # [OS/2] yStrikeoutSize
        averageWidth = 0            # [OS/2] xAvgCharWidth
        superscriptXSize = 0        # [OS/2] ySuperscriptXSize
        superscriptXOffset = 0      # [OS/2] ySubscriptXOffset
        superscriptYSize = 0        # [OS/2] ySuperscriptYSize
        superscriptYOffset = 0      # [OS/2] ySuperscriptYOffset
        subscriptXSize = 0          # [OS/2] ySubscriptXSize
        subscriptXOffset = 0        # [OS/2] ySubscriptXOffset
        subscriptYSize = 0          # [OS/2] ySubscriptYSize
        subscriptYOffset = 0        # [OS/2] ySubscriptYOffset
        underlinePosition = 0       # [post] underlinePosition
        underlineThickness = 0      # [post] underlineThickness
        italicAngle = 0             # [post] italicAngle


def main(maps):

    for map in maps:
        if ":" in map:
            map_list = map.split(':')
            if len(map_list) == 2:
                fontpath = map_list[0]
                expectedpath = map_list[1]
                if os.path.isfile(fontpath):
                    if os.path.isfile(expectedpath):
                        try:
                            expected_stream = open(expectedpath, "r")
                            expected_dict = load(expected_stream, Loader=Loader)
                            print(expected_dict)
                            sys.exit(0)

                            # TODO : parse YAML file for expected data
                        except Exception as e:
                            pass

                        try:
                            tt = ttLib.TTFont(fontpath)

                            # TODO: parse font OpenType tables for comparison data
                        except Exception as e:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass





if __name__ == '__main__':
    main(sys.argv[1:])
