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
    def __init__(self, filepath):
        self.filepath = filepath         # path to the font
        self.font_object = None          # fontTools TTFont object
        self.unitsPerEm = 0              # [head] unitsPerEm
        self.ascent = 0                  # [hhea] ascent
        self.descent = 0                 # [hhea] descent
        self.lineGap = 0                 # [hhea] lineGap
        self.capheight = 0               # [OS/2] sCapHeight
        self.xheight = 0                 # [OS/2] sxHeight
        self.typoAscender = 0            # [OS/2] sTypoAscender
        self.typoDescender = 0           # [OS/2] sTypoDescender
        self.typoLineGap = 0             # [OS/2] sTypoLineGap
        self.winAscent = 0               # [OS/2] usWinDescent
        self.winDescent = 0              # [OS/2] usWinAscent
        self.strikeoutPosition = 0       # [OS/2] yStrikeoutPosition
        self.strikeoutSize = 0           # [OS/2] yStrikeoutSize
        self.averageWidth = 0            # [OS/2] xAvgCharWidth
        self.superscriptXSize = 0        # [OS/2] ySuperscriptXSize
        self.superscriptXOffset = 0      # [OS/2] ySubscriptXOffset
        self.superscriptYSize = 0        # [OS/2] ySuperscriptYSize
        self.superscriptYOffset = 0      # [OS/2] ySuperscriptYOffset
        self.subscriptXSize = 0          # [OS/2] ySubscriptXSize
        self.subscriptXOffset = 0        # [OS/2] ySubscriptXOffset
        self.subscriptYSize = 0          # [OS/2] ySubscriptYSize
        self.subscriptYOffset = 0        # [OS/2] ySubscriptYOffset
        self.underlinePosition = 0       # [post] underlinePosition
        self.underlineThickness = 0      # [post] underlineThickness
        self.italicAngle = 0             # [post] italicAngle

        # define metrics properties of the instance
        self.create_metrics_object_from_font(self.filepath)


    def create_metrics_object_from_font(self, fontpath):
        self.font_object = ttLib.TTFont(fontpath)
        self.define_head_table()

    def define_head_table(self):
        self.unitsPerEm = self.font_object['head'].__dict__['unitsPerEm']


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
                            # parse the expected font metrics
                            expected_stream = open(expectedpath, "r")
                            expected_dict = load(expected_stream, Loader=Loader)

                            # create the observed font metrics object
                            observed_metrics = MetricsObject(fontpath)
                        except Exception as e:
                            sys.stderr.write("Error: " + str(e))
                    else:
                        sys.stderr.write("Error: The requested path to the expected metrics does not appear to be a file")
                        sys.exit(1)
                else:
                    sys.stderr.write("Error: The requested path to the font does not appear to be a file")
                    sys.exit(1)
            else:
                sys.stderr.write("Error: Please define the paths to the font file and the expected metrics YAML file in the argument")
                sys.exit(1)
        else:
            sys.stderr.write("Error: incorrect syntax for the definition of the font and expected metrics YAML file paths")
            sys.exit(1)





if __name__ == '__main__':
    main(sys.argv[1:])
