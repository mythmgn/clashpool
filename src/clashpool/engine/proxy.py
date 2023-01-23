#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:
    clash proxy
"""
import copy
import time
from cup import log

class ClashProxy:
    """clash proxy"""
    _REQUIRE_SER_KEYS = [
        'name',
        'type',
        'server',
        'port',
        'type'
    ]

    def __init__(self, yaml_kvs):
        """
        :param name:
            name of the proxy

        :raise Exception:
            ValueError if name not in yaml_kvs
        """
        ClashProxy.check_valid_serverstring(yaml_kvs)
        self._attrs = copy.deepcopy(yaml_kvs)
        self._time = time.time()
        self._name = self._attrs['name']
        self._type = self._attrs['type']
        self._uniqid = f'{self._attrs["server"]}:{self._attrs["port"]}'
        self._info = f'{self._name}(type {self._type}, service {self._uniqid}'
        self._kvs = yaml_kvs

    @staticmethod
    def check_valid_serverstring(kvs):
        """
        class static method for check serverstring
        """
        for key in ClashProxy._REQUIRE_SER_KEYS:
            if key not in kvs:
                raise ValueError(f'{key} not set')

    def ctime(self):
        """
        return date
        """
        return self._time

    def name(self):
        """
        get name of the proxy
        """
        return self._name

    def refresh_expiration(self):
        """
        refresh expiration time
        """
        self._time = time.time()
        log.info(
            f'expiration refresh {self._name}:{self._uniqid}'
        )

    def unique_id(self):
        """
        get unique id of the proxy
        """
        return self._uniqid

    def info(self):
        """string info of the server"""
        return self._info

    def attrs(self):
        """return attrs in kv"""
        return self._kvs


# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
