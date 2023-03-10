#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:
    Use Jinja2 to handle function mappings
"""
# import abc
import datetime

from cup import decorators


def date_current(inputstring):
    """
    input with a string and replace {%date:YYYY/MM/DD%} with real time
    """
    return datetime.datetime.today().strftime(inputstring)


@decorators.Singleton
class Func2JinjaMappings:
    """function 2 jinja2 mappings"""
    _MAPPINGS = {}

    def __init__(self):
        self.add_func('date_current', date_current)

    @classmethod
    def add_func(cls, name, func):
        """
        add func for this
        """
        if not callable(func):
            raise ValueError(f'func not callable {func}')
        cls._MAPPINGS[name] = func

    @classmethod
    def mappings(cls) -> dict:
        """return func mappings"""
        return cls._MAPPINGS


# def func_handle(inputstring):
#     """
#     return func string
#
#     :raise Exception:
#         ValueError
#     """
#     if not isinstance(inputstring, str):
#         raise ValueError('intputstring not a str')
#     firstind = inputstring.find('{{')
#     lastind = inputstring.rfind('}}')
#     if any([firstind < 0, lastind < 0, inputstring is None]):
#         # no need to use func to handle
#         return inputstring
#     index = firstind
#     length = len(inputstring)
#     while index < length:
#         # replace(index, length)
#         tmplen = inputstring.find('}}')


# vi:set tw=0 ts=4 sw=4 nowrap fdm=indent
