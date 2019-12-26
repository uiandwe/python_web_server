# -*- coding: utf-8 -*-
# https://www.slideshare.net/kwatch/how-to-make-the-fastest-router-in-python

import re


class Router:
    def __init__(self, mapping):
        self.mapping_list = [(re.compile(path), klass, funcs) for path, klass, funcs in mapping]

    def lookup(self, req_method, req_path):
        for rexp, klass, funcs in self.mapping_list:
            m = rexp.match(req_path)
            if m:
                parms = [int(v) for v in m.groups()]
                func = funcs.get(req_method)
                return klass, func, parms

        return None, None, None


if __name__ == '__main__':
    # path, class, {method: func,}
    from apis.books import BooksAPI
    from apis.orders import OrdersApi

    mapping_list = [
        (r"/api/books/", BooksAPI, {"GET": BooksAPI.do_index, "POST": BooksAPI.do_create}),
        (r"/api/orders/", OrdersApi, {"GET": OrdersApi.do_show, "POST": OrdersApi.do_update})
    ]

    router = Router(mapping_list)
    assert router.lookup("GET", "/api/books/") == (BooksAPI, BooksAPI.do_index, [])
    # assert router.lookup("GET", "/api/books/123/") == (BooksAPI, BooksAPI.do_index, [123])
    # assert router.lookup("GET", "api/books/123/test/") == (None, None, None)
