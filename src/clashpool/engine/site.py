#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:

"""
import yaml
import requests
from cup import log

from clashpool.engine import proxy

class UrlConfigProvider:
    """
    Clash Config(config.yaml) Provider which can be fetched by url.
    """
    def __init__(self, name: str, expire_secs: int, url: str, urltimeout: int):
        """
        """
        self._name = name
        self._url = url
        self._expire_secs = expire_secs
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
        log.info(f'to fetch UrlConfigProvider {self._name} for {self._url}')
        try:
            req = requests.get(self._url, timeout=self._urltimeout)
        except requests.RequestException as errinfo:
            log.warn(f'failed to get url site {self._url} {errinfo}, return')
            return []
        if req.status_code != 200:
            # pylint: disable= too-few-public-methods
            log.warn(f'UrlConfigProvider {self._name} fetch url fail, return')
            return []
        kvs = None
        decode_info = req.content.decode().replace('!', 'WRONG_LINE_REPLACED')
        decode_info = decode_info.replace('<str>', 'WRONG_LINE_REPLACED')
        try:
            kvs = yaml.load(decode_info, Loader=yaml.FullLoader)
            if not isinstance(kvs, dict):
                return []
        # pylint: disable=broad-except
        except Exception:
            log.warn(
                f'UrlConfigProvider {self._name} failed to '
                'parse {self._url}: {err}'
            )
            return []
        tmplist = kvs.get('proxies')
        if tmplist is None:
            log.warn(
                f'UrlConfigProvider {self._name} no proxies found, return'
            )
            return []
        proxies = []
        for tmp in tmplist:
            try:
                pro = proxy.ClashProxy(tmp)
                if any([
                    pro.name().find('CN') >= 0,
                    pro.name().find('中国') >=0
                ]):
                    log.info(f'skip proxy back to china line {pro.name()}')
                    continue
                proxies.append(pro)
                log.info(f'proxy({pro.info()}) added')
            except ValueError:
                log.warn('ignore the proxy, continue')
        log.info(f'fetch proxy for site {self._name} done')
        return proxies

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
