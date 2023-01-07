#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:

"""
from clashpool.engine import pool


man = pool.PoolManager('./conf/clashpool.toml', 100)
man.start()


# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent

