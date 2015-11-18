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
    """A font metrics object that maintains metrics properties during testing"""
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
    """Performs metrics tests on fonts vs. expected values in a YAML settings file"""

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
                            ERROR_OCCURRED = False
                            # parse the expected font metrics
                            expected_stream = open(expectedpath, "r")
                            expected_metrics = load(expected_stream, Loader=Loader)

                            # create the observed font metrics object
                            observed_metrics = MetricsObject(fontpath)

                            # font report header
                            print("Font Metrics Tests for '" + fontpath + "'")

                            # Units per Em Test
                            if not observed_metrics.unitsPerEm == expected_metrics['unitsPerEm']:
                                sys.stderr.write("  X [head] ERROR: unitsPerEm values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [head] Units per Em")

                            # hhea Ascent Test
                            if not observed_metrics.ascent == expected_metrics['ascent']:
                                sys.stderr.write("  X [hhea] ERROR: hhea table Ascent values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [hhea] Ascent")

                            # hhea Descent Test
                            if not observed_metrics.descent == expected_metrics['descent']:
                                sys.stderr.write("  X [hhea] ERROR: hhea table Descent values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [hhea] Descent")

                            # hhea Linegap test
                            if not observed_metrics.lineGap == expected_metrics['lineGap']:
                                sys.stderr.write("  X [hhea] ERROR: hhea table lineGap values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [hhea] Linegap")

                            # Cap Height Test
                            if not observed_metrics.capheight == expected_metrics['capHeight']:
                                sys.stderr.write("  X [OS/2] ERROR: Cap Height values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Cap Height")

                            # X Height Test
                            if not observed_metrics.xheight == expected_metrics['xHeight']:
                                sys.stderr.write("  X [OS/2] ERROR: X Height values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] X Height")

                            # Typo Ascender Test
                            if not observed_metrics.typoAscender == expected_metrics['typoAscender']:
                                sys.stderr.write("  X [OS/2] ERROR: Typo Ascender values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Typo Ascender")

                            # Typo Descender Test
                            if not observed_metrics.typoDescender == expected_metrics['typoDescender']:
                                sys.stderr.write("  X [OS/2] ERROR: Typo Descender values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Typo Descender")

                            # Typo Linegap Test
                            if not observed_metrics.typoLineGap == expected_metrics['typoLineGap']:
                                sys.stderr.write("  X [OS/2] ERROR: Typo Linegap values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Typo Linegap")

                            # winAscent Test
                            if not observed_metrics.winAscent == expected_metrics['winAscent']:
                                sys.stderr.write("  X [OS/2] ERROR: winAscent values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] winAscent")

                            # winDescent Test
                            if not observed_metrics.winDescent == expected_metrics['winDescent']:
                                sys.stderr.write("  X [OS/2] ERROR: winDescent values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] winDescent")

                            # Strikeout Position Test
                            if not observed_metrics.strikeoutPosition == expected_metrics['strikeoutPosition']:
                                sys.stderr.write("  X [OS/2] ERROR: Strikeout Position values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Strikeout Position")

                            # Strikeout Size test
                            if not observed_metrics.strikeoutSize == expected_metrics['strikeoutSize']:
                                sys.stderr.write("  X [OS/2] ERROR: Strikeout Size values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Strikeout Size")

                            # Average Character Width Test
                            if not observed_metrics.averageWidth == expected_metrics['averageWidth']:
                                sys.stderr.write("  X [OS/2] ERROR: Average Character Width values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Average Character Width")

                            # Superscript X Size Test
                            if not observed_metrics.superscriptXSize == expected_metrics['superscriptXSize']:
                                sys.stderr.write("  X [OS/2] ERROR: Superscript X Size values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Superscript X Size")

                            # Superscript X Offset Test
                            if not observed_metrics.superscriptXOffset == expected_metrics['superscriptXOffset']:
                                sys.stderr.write("  X [OS/2] ERROR: Superscript X Offset values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Superscript X Offset")

                            # Superscript Y Size Test
                            if not observed_metrics.superscriptYSize == expected_metrics['superscriptYSize']:
                                sys.stderr.write("  X [OS/2] ERROR: Superscript Y Size values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Superscript Y Size")

                            # Superscript Y Offset Test
                            if not observed_metrics.superscriptYOffset == expected_metrics['superscriptYOffset']:
                                sys.stderr.write("  X [OS/2] ERROR: Superscript Y Offset values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Superscript Y Offset")

                            # Subscript X Size Test
                            if not observed_metrics.subscriptXSize == expected_metrics['subscriptXSize']:
                                sys.stderr.write("  X [OS/2] ERROR: Subscript X Size values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Subscript X Size")

                            # Subscript X Offset Test
                            if not observed_metrics.subscriptXOffset == expected_metrics['subscriptXOffset']:
                                sys.stderr.write("  X [OS/2] ERROR: Subscript X Offset values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Subscript X Offset")

                            # Subscript Y Size Test
                            if not observed_metrics.subscriptYSize == expected_metrics['subscriptYSize']:
                                sys.stderr.write("  X [OS/2] ERROR: Subscript Y Size values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Subscript Y Size")

                            # Subscript X Offset Test
                            if not observed_metrics.subscriptYOffset == expected_metrics['subscriptYOffset']:
                                sys.stderr.write("  X [OS/2] ERROR: Subscript Y Offset values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [OS/2] Subscript Y Offset")

                            # Underline Posiiton Test
                            if not observed_metrics.underlinePosition == expected_metrics['underlinePosition']:
                                sys.stderr.write("  X [post] ERROR: Underline Position values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [post] Underline Position")

                            # Underline Posiiton Test
                            if not observed_metrics.underlineThickness == expected_metrics['underlineThickness']:
                                sys.stderr.write("  X [post] ERROR: Underline Thickness values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [post] Underline Thickness")

                            # Italic Angle Test
                            if not observed_metrics.italicAngle == expected_metrics['italicAngle']:
                                sys.stderr.write("  X [post] ERROR: Italic Angle values do not match\n")
                                ERROR_OCCURRED = True
                            else:
                                print("  ✓ [post] Italic Angle")

                            # Raise appropriate exit code based upon success of all tests
                            if ERROR_OCCURRED == True:
                                sys.exit(1)
                            else:
                                sys.exit(0)

                        except Exception as e:
                            sys.stderr.write("ERROR: " + str(e))
                            sys.exit(1)
                    else:
                        sys.stderr.write("ERROR: The requested path to the expected metrics YAML file does not appear to be a file")
                        sys.exit(1)
                else:
                    sys.stderr.write("ERROR: The requested path to the font does not appear to be a file")
                    sys.exit(1)
            else:
                sys.stderr.write("ERROR: Please define the paths to the font file and the expected metrics YAML file in the argument")
                sys.exit(1)
        else:
            sys.stderr.write("ERROR: incorrect syntax for the command line definition of the font and expected metrics YAML file paths")
            sys.exit(1)

# YAML stub file text
yaml_stub = """
# [FONT PATH]

# [head] table
unitsPerEm:

# [hhea] table
descent:
ascent:
lineGap:

# [OS/2] table
capHeight:
xHeight:
typoAscender:
typoDescender:
typoLineGap:
winAscent:
winDescent:
strikeoutPosition:
strikeoutSize:
averageWidth:
superscriptXSize:
superscriptXOffset:
superscriptYSize:
superscriptYOffset:
subscriptXSize:
subscriptXOffset:
subscriptYSize:
subscriptYOffset:

# [post] table
underlinePosition:
underlineThickness:
italicAngle:
"""

def write_stubfile():
    """Writes a metrics YAML stub file in the root directory"""
    try:
        with open("metrics.yaml", 'wt') as writer:
            writer.write(yaml_stub)
        print("[test-metrics.py] Metrics YAML stub file was successfully created on the path 'metrics.yaml'")
    except Exception as e:
        sys.stderr.write("[test-metrics.py] ERROR: Unable to generate file stub. " + str(e))
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 0:
        if sys.argv[1].lower() == "stub":
            write_stubfile()
        else:
            main(sys.argv[1:])
