# -*- coding: utf-8 -*-
from http_handler.methods import Methods


class BooksAPI(Methods):
    @staticmethod
    def do_index(req):
        print("do_index")

    @staticmethod
    def do_create(req):
        print("do_create")
