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
import collections

import tomlkit
from tomlkit import exceptions
import jinja2
import yaml
import requests
from cup import log
from cup import decorators

from clashpool.engine import func
from clashpool.engine import site
from clashpool.engine import proxy


@decorators.Singleton
class PoolManager:
    """clash pool manager"""
    EXPIRE_DAYS = 4
    EXPIRE_SECONDS = EXPIRE_DAYS * 24 * 3600

    def __init__(self, confloc: str, max_proxy_count: int = 1000):
        """
        pool manager

        :raise Exception:
            IOError if confloc not exist
        """
        if not os.path.exists(confloc):
            raise IOError('conf not exist({})'.format(confloc))
        self._confloc = confloc
        self._proxies = collections.OrderedDict()
        self._sortqueue = queue.PriorityQueue(max_proxy_count)
        self._sites = []
        self._stop_sign = False
        self._running = False
        self._conf_toml = None
        self._yamlkvs = {}
        self._max_proxycount = max_proxy_count
        self._refresh_conf_with_jinjafunc()
        log.init_comlog(
            'clashpool',
            logfile=f"{self._conf_toml['global']['workdir']}/log/clashpool.log"
        )
        self._running = True

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

    def running(self):
        """is running"""
        return self._running

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

    def serve(self):
        """start the pool"""
        while not self.needstop():
            self._refresh_conf_with_jinjafunc()
            self._proc_sites()
            time.sleep(self._conf_toml['proxies']['fetch-interval'])
        self._running = False

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
                single['name'], self.EXPIRE_SECONDS, single['url'],
                self._conf_toml['proxies']['url-timeout']
            )
            proxies = siteobj.fetch_proxies()
        for pro in proxies:
            uid = pro.unique_id()
            if uid in self._proxies:
                self._proxies[uid].refresh_expiration()
            else:
                self._proxies[uid] = pro
                self._sortqueue.put((pro.ctime(), pro))
        self._handle_expired()

    def _handle_expired(self):
        """remove expired proxies from the queue"""
        log.info('to check if the proxies have expired')
        item = None
        while not self._sortqueue.empty():
            try:
                _, item = self._sortqueue.get_nowait()
            except queue.Empty as errinfo:
                log.info('no proxy available yet, no need handle expiration')
                break
            if (time.time() - item.ctime()) > self.EXPIRE_SECONDS:
                log.warning(f'proxy expired, to remove it {item.info}')
                del self._proxies[item.unique_id()]
            else:
                self._sortqueue.put((item.ctime(), item))
                log.info(f'proxy not expired {item.info()}, return')
                break

    def proxies(self):
        """get unique and valid procies"""
        tmplist = []
        for _, item in self._proxies.items():
            tmplist.append(item)
        return tmplist

    def bindinfo(self):
        """return bind info  (server: str, port: int)"""
        return (
            self._conf_toml['global']['server'],
            self._conf_toml['global']['port']
        )


# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
