# -*- coding: utf-8 -*-
import inspect


class Methods:
    @classmethod
    def do_options(cls, req):
        return inspect.getmembers(cls, predicate=inspect.ismethod)

    @staticmethod
    def do_head(req):
        return ''
