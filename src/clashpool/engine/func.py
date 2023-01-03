#!/usr/bin/env python
# -*- coding: utf-8 -*
# Copyright: See LICENSE for details.
# Authors: Guannan Ma (@mythmgn),
"""
:description:
    Use Jinja2 to handle function mappings
"""
import abc
import jinja2
import datetime

from cup import decorations


class BaseFunc(abc.ABC):
    """
    Abstract class:BaseFunc
    """

    @abc.abstractmethod
    def functional(self, inputstring):
        """functional string"""


class Date(BaseFunc):
    """
    input with a string and replace {%date:YYYY/MM/DD%} with real time
    """

    @classmethod
    def functional(inputstring):
        """
        :return:
            return the specified format for inputstring
        """
        return datetime.datetime.today().strftime(inputstring)


@decorations.Singleton
class Func2JinjaMappings:
    _MAPPINGS = {}

    def __init__(self):
        Func2JinjaMappings.add_func('date', Date.functional)

    @classmethod
    def add_func(name, func):
        """
        add func for this
        """
        if not callable(func):
            raise ValueError('func not callable {}'.format(func))
        _MAPPINGS[func.func_name] = func

    @classmethod
    def mappings() -> list:
        return _MAPPINGS


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
