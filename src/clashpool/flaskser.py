#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:
    flask http server
"""
import time
import yaml
import collections

import flask
from flask import request
import waitress
from cup import thread
from clashpool.engine import pool

app = flask.Flask(__name__)


def appserve(confloc: str):
    """create app for flask apps"""
    poolman = pool.PoolManager(confloc, 100)
    thd = thread.CupThread(target=poolman.serve)
    thd.start()
    while not poolman.running():
        time.sleep(1)
    bindhost, port = poolman.bindinfo()
    waitress.serve(app, host=bindhost, port=port)


@app.route('/')
def index():
    """index"""
    return 'Index Page'


@app.route('/proxies/<media_type>')
def proxies_yaml(media_type):
    """return proxies with yaml"""
    poolman = pool.PoolManager('')
    proxies = poolman.proxies()
    if media_type == 'yaml':
        kvs = {}
        kvs['proxies'] = []
        for item in proxies:
            kvs['proxies'].append(item.attrs())
        return flask.Response(
            yaml.dump(kvs, encoding='utf-8', allow_unicode=True),
            status=200,  mimetype='application/yaml'
        )
    return flask.abort(400)

# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
