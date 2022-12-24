#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:

"""
import collections


TYPE = [
    'URL',
]

CrawTask = collections.namedtuple(
    'CrawTask', ['id', 'type', 'url', 'proxies', ']
)

class Crawler(object):
    """crawler"""

    def run(self):
        """run the crawler"""

    def stop(self, delay=0):
        """
        :param delay:
            stop after `delay` seconds

        """


# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
