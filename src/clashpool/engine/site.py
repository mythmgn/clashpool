#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:

"""
import requests
import yaml
from cup import log

from clashpool.engine import proxy
from clashpool.engine import func

class UrlConfigProvider:
    """
    Clash Config(config.yaml) Provider which can be fetched by url.
    """
    def __init__(self, name: str, expire_days: int, url: str, urltimeout: int):
        """
        """
        self._name = name
        self._url = func.func_handle(url)
        self._expire_days = expire_days
        self._proxies = None
        self._urltimeout = urltimeout

    def fetch_proxies(self) -> list:
        """
        return pool list

        :return:
            return None if error occurs, otherwise proxy list
        """
        # if it's None, will try fetch again
        if self._proxies is not None:
            return self._proxies
        log.info(
            'to fetch UrlConfigProvider {0} for {1}'.format(
                self._name, self._url))
        req = requests.get(self._url, timeout=3)
        if req.status_code != 200:
            # pylint: disable= too-few-public-methods
            log.warn('UrlConfigProvider {} fetch url fail'.format(self._name))
            return None
        kvs = None
        try:
            kvs = yaml.load(req.content.decode(), Loader=yaml.BaseLoader)
        # pylint: disable=broad-except
        except Exception as err:
            log.warn('UrlConfigProvider {0} failed to parse {1}: {2}'.format(
                self._name, self._url, err
            ))
            return None
        tmplist = kvs.get('proxies')
        if tmplist is None:
            log.warn(
                'UrlConfigProvider {0} no proxies found'.format(self._name)
            )
        proxies = []
        for tmp in tmplist:
            try:
                proxies.append(proxy.ClashProxy(tmp))
            except ValueError:
                log.warn('ignore the proxy, continue')
        return proxies
# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
