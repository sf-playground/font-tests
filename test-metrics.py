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
        pass

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
