#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:

"""
# pylint: disable=unused-import too-few-public-methods deprecated-method
# import datetime
import os
import time
import copy
import queue
try:
    # pylint disable: W05
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


import jinja2
import yaml
import requests
from cup import log

from clashpool.engine import func
from clashpool.engine import site
from clashpool.engine import proxy


class PoolManager:
    """clash pool manager"""
    def __init__(self, confloc : str, max_proxy_count: int = 1000):
        """
        pool manager

        :raise Exception:
            IOError if confloc not exist
        """
        if not os.path.exists(confloc):
            raise IOError('conf not exist({})'.format(confloc))
        self._confloc = confloc
        self._proxies = {}
        self._queue = queue.PriorityQueue(max_proxy_count)
        self._sites = []
        self._stop_sign = False
        self._conf_toml = None
        self._yamlkvs = {}

    def _refresh_conf_with_jinjafunc(self):
        """
        will translate toml conf into real values
        """
        tmpldir = os.path.dirname(self._confloc)
        tmplname = os.path.basename(self._confloc)
        env = jinja2.Environment(loader=FileSystemLoader(tmpldir))
        jinjatempl = env.get_template(tmplname)
        jinjatempl.globals.update(func.Func2JinjaMappings.mappings())
        tmplstring = jinja_template.render()
        try:
            tmp_confdict = tomllib.loads(tmplstring)
            self._conf_toml = tmp_confdict
        except tomllib.TOMLDecodeError as err:
            log.warning(f'to toml conf failed:{self._confloc} {err}')

    def stop(self, delay_time: int = 2):
        """
        stop the manager after delay_time
        """
        self._stop_sign = True

    def start(self, threadmax=4):
        """start the pool"""
        while not self._stop_sign:
            self._refresh_conf_with_jinjafunc()

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
