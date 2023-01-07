#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:

"""
# pylint: disable=unused-import too-few-public-methods
# pylint: disable=deprecated-method,too-many-instance-attributes
# import datetime
import os
import time
import copy
import queue
import tomlkit
from tomlkit import exceptions
# try:
#     # pylint disable: W05
#     import tomllib
# except ModuleNotFoundError:
#     import tomli as tomllib


import jinja2
import yaml
import requests
from cup import log

from clashpool.engine import func
from clashpool.engine import site
from clashpool.engine import proxy


class PoolManager:
    """clash pool manager"""
    EXPIRE_DAYS = 4
    EXPIRE_SECONDS = EXPIRE_DAYS * 24 * 3600

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
        self._sortqueue = queue.PriorityQueue(max_proxy_count)
        self._sites = []
        self._stop_sign = False
        self._conf_toml = None
        self._yamlkvs = {}
        self._max_proxycount = max_proxy_count

    def _refresh_conf_with_jinjafunc(self):
        """
        will translate toml conf into real values
        """
        tmpldir = os.path.dirname(self._confloc)
        tmplname = os.path.basename(self._confloc)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(tmpldir))
        jinjatempl = env.get_template(tmplname)
        jinjatempl.globals.update(func.Func2JinjaMappings().mappings())
        tmplstring = jinjatempl.render()
        try:
            tmp_confdict = tomlkit.loads(tmplstring)
            self._conf_toml = tmp_confdict
        except exceptions.ParseError as err:
            log.warning(f'to toml conf failed:{self._confloc} {err}')

    def stop(self):
        """
        stop the manager after delay_time
        """
        self._stop_sign = True
        log.info('to stop the clash pool')

    def needstop(self):
        """
        check if need stop
        """
        return self._stop_sign

    # def start(self, threadmax=4):
    def start(self):
        """start the pool"""
        while not self.needstop():
            self._refresh_conf_with_jinjafunc()
            self._proc_sites()
            time.sleep(3)
            print(self.proxies())

    def _proc_sites(self):
        """
        proc sites
        """
        if self.needstop():
            log.info('need stop, proc site return')
            return
        if self._conf_toml is None:
            log.error('cannot proc sites as toml parsing failed')
            self.stop()
            return
        for single in self._conf_toml['proxies']['sites']:
            siteobj = site.UrlConfigProvider(
                single['name'], PoolManager.EXPIRE_DAYS, single['url'],
                self._conf_toml['global']['timeout']
            )
            proxies = siteobj.fetch_proxies()
        for pro in proxies:
            uid = pro.unique_id()
            if uid in self._proxies:
                self._proxies[uid].refresh_expiration()
            else:
                self._proxies[uid] = pro
        self._handle_expired()

    def _handle_expired(self):
        """remove expired proxies from the queue"""
        ctime = None
        item = None
        while not self._sortqueue.empty():
            try:
                ctime, item = self._sortqueue.get_nowait()
            except queue.Empty as errinfo:
                log.info('no proxy available yet, no need handle expiration')
                break
            if (item.ctime() - time.time()) > PoolManager.EXPIRE_SECONDS:
                log.warning(f'proxy expired, to remove it {item.info}')
                del self._proxies[item.unique_id()]
            else:
                self._sortqueue.put((item.ctime(), item))
                break

    def proxies(self):
        """get unique and valid procies"""
        return self._proxies.items()

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
