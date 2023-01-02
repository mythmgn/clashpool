#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:

"""
# pylint: disable=unused-import too-few-public-methods deprecated-method
# import datetime

import time
import copy
import queue
try:
    # pylint disable: W05
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from cup import log
import requests
import yaml

from clashpool.engine import site
from clashpool.engine import proxy



class PoolManager:
    """clash pool manager"""
    def __init__(self, max_proxy_count: int = 1000, ):
        """pool manager"""
        self._proxies = {}
        self._queue = queue.PriorityQueue(max_proxy_count)
        self._sites = []

    def stop(self, delay_time: int = 2):
        """
        stop the manager after delay_time
        """

    def start(self, threadmax=4):
        """start the pool"""

    def proc_sites(self, sitesinfo):
        """
        proc sites
        """

    def _make_unique(self):
        """
        reorgnize the whole thing
        """

    def proxies(self):
        """get unique and valid procies"""

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
