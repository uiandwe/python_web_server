# -*- coding: utf-8 -*-
from http_handler.methods import Methods


class BooksAPI(Methods):
    @staticmethod
    def do_index():
        print("do_index")

    @staticmethod
    def do_create():
        print("do_create")
