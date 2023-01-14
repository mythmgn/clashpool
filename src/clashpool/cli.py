#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:

"""
import argparse
from clashpool import flaskser


def main():
    """
    main entry
    """
    parser = argparse.ArgumentParser(description='Clashpool')
    parser.add_argument(
        '-c', '--conf', required=True,
        type=str,
        help='configuration file which specify core params'
    )
    args = parser.parse_args()
    flaskser.appserve(args.conf)


# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
