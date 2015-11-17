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


# TODO : create metrics YAML file stub with proper definition fields

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
        self.winAscent = 0               # [OS/2] usWinAscent
        self.winDescent = 0              # [OS/2] usWinDescent
        self.strikeoutPosition = 0       # [OS/2] yStrikeoutPosition
        self.strikeoutSize = 0           # [OS/2] yStrikeoutSize
        self.averageWidth = 0            # [OS/2] xAvgCharWidth
        self.superscriptXSize = 0        # [OS/2] ySuperscriptXSize
        self.superscriptXOffset = 0      # [OS/2] ySuperscriptXOffset
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
        self.define_hhea_table()
        self.define_os2_table()
        self.define_post_table()

    def define_head_table(self):
        try:
            self.unitsPerEm = self.font_object['head'].__dict__['unitsPerEm']
        except Exception as e:
            sys.stderr.write("Error: " + str(e))

    def define_hhea_table(self):
        try:
            hhea_table_dict = self.font_object['hhea'].__dict__
            self.ascent = hhea_table_dict['ascent']
            self.descent = hhea_table_dict['descent']
            self.lineGap = hhea_table_dict['lineGap']
        except Exception as e:
            sys.stderr.write("Error: " + str(e))

    def define_os2_table(self):
        try:
            os2_table_dict = self.font_object['OS/2'].__dict__
            self.capheight = os2_table_dict['sCapHeight']
            self.xheight = os2_table_dict['sxHeight']
            self.typoAscender = os2_table_dict['sTypoAscender']
            self.typoDescender = os2_table_dict['sTypoDescender']
            self.typoLineGap = os2_table_dict['sTypoLineGap']
            self.winAscent = os2_table_dict['usWinAscent']
            self.winDescent = os2_table_dict['usWinDescent']
            self.strikeoutPosition = os2_table_dict['yStrikeoutPosition']
            self.strikeoutSize = os2_table_dict['yStrikeoutSize']
            self.averageWidth = os2_table_dict['xAvgCharWidth']
            self.superscriptXSize = os2_table_dict['ySuperscriptXSize']
            self.superscriptXOffset = os2_table_dict['ySuperscriptXOffset']
            self.superscriptYSize = os2_table_dict['ySuperscriptYSize']
            self.superscriptYOffset = os2_table_dict['ySuperscriptYOffset']
            self.subscriptXSize = os2_table_dict['ySubscriptXSize']
            self.subscriptXOffset = os2_table_dict['ySubscriptXOffset']
            self.subscriptYSize = os2_table_dict['ySubscriptYSize']
            self.subscriptYOffset = os2_table_dict['ySubscriptYOffset']
        except Exception as e:
            sys.stderr.write("Error: " + str(e))

    def define_post_table(self):
        try:
            post_table_dict = self.font_object['post'].__dict__
            self.underlinePosition = post_table_dict['underlinePosition']
            self.underlineThickness = post_table_dict['underlineThickness']
            self.italicAngle = post_table_dict['italicAngle']
        except Exception as e:
            sys.stderr.write("Error: " + str(e))


def main(maps):

    # Begin report
    print("\nBegin test-metrics.py font metrics tests\n")

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
                            expected_metrics = load(expected_stream, Loader=Loader)

                            # create the observed font metrics object
                            observed_metrics = MetricsObject(fontpath)

                            # font report header
                            print("Font Metrics Tests for '" + fontpath + "'")

                            if not observed_metrics.unitsPerEm == expected_metrics['unitsPerEm']:
                                sys.stderr.write("[test-metrics.py] Error: unitsPerEm values do not match ")
                                sys.exit(1)
                            else:
                                print("  ✓ [head] Units per Em")

                            if not observed_metrics.ascent == expected_metrics['ascent']:
                                sys.stderr.write("[test-metrics.py] Error: hhea table Ascent values do not match ")
                                sys.exit(1)
                            else:
                                print("  ✓ [hhea] Ascent")

                            if not observed_metrics.descent == expected_metrics['descent']:
                                sys.stderr.write("[test-metrics.py] Error: hhea table Descent values do not match ")
                                sys.exit(1)
                            else:
                                print("  ✓ [hhea] Descent")

                            if not observed_metrics.lineGap == expected_metrics['lineGap']:
                                sys.stderr.write("[test-metrics.py] Error: hhea table lineGap values do not match ")
                                sys.exit(1)
                            else:
                                print("  ✓ [hhea] Linegap")


                        except Exception as e:
                            sys.stderr.write("Error: " + str(e))
                    else:
                        sys.stderr.write("Error: The requested path to the expected metrics YAML file does not appear to be a file")
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
