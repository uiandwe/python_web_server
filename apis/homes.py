# -*- coding: utf-8 -*-
from http.render import RenderHandler
from logger import Logger

LOG = Logger().log

__all__ = (
    'HomesAPI'
)


class HomesAPI:

    @classmethod
    def do_index(cls):
        return RenderHandler(cls.__name__, 'index.html')()

    @staticmethod
    def do_create():
        print("home do_create")
