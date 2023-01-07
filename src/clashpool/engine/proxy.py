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
        self._uniqid = '{0}:{1}'.format(
            self._attrs['server'], self._attrs['port']
        )
        self._info = '{0}(type {1}, service {2}'.format(
            self._name, self._type, self._uniqid
        )

    @staticmethod
    def check_valid_serverstring(kvs):
        """
        class static method for check serverstring
        """
        for key in ClashProxy._REQUIRE_SER_KEYS:
            if key not in kvs:
                raise ValueError('{0} not set'.format(key))

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
            'expiration refresh {0}:{1}'.format(self.name(), self.unique_id())
        )

    def unique_id(self):
        """
        get unique id of the proxy
        """
        return self._uniqid

    def info(self):
        """string info of the server"""
        return self._info


# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
