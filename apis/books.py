# -*- coding: utf-8 -*-
from http_handler.methods import Methods

__all__ = (
    'BooksAPI'
)


class BooksAPI(Methods):
    @staticmethod
    def do_index(req):
        print("do_index")
        return ''

    @staticmethod
    def do_create(req):
        print("do_create")
        return ''
