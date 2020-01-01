# -*- coding: utf-8 -*-
import inspect


class Methods:
    @classmethod
    def do_options(cls, req):
        return inspect.getmembers(cls, predicate=inspect.ismethod)

    @classmethod
    def do_head(cls, req):
        return ''
