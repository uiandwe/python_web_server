# -*- coding: utf-8 -*-

from http_handler.methods import Methods
from http_handler.render import RenderHandler
from logger import Logger

LOG = Logger().log

__all__ = (
    'HomesAPI'
)


class HomesAPI(Methods):

    @staticmethod
    def do_index(req):
        return RenderHandler(HomesAPI.__name__, 'index.html')()

    @staticmethod
    def do_create(req):
        print("home do_create")
