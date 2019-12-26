# -*- coding: utf-8 -*-
# https://www.slideshare.net/kwatch/how-to-make-the-fastest-router-in-python

import re


def prefix_str(s):
    return s.split('{', 1)[0]


class Router:
    def __init__(self, mapping):
        self.mapping_list = []
        self.mapping_dict = {}
        for path, klass, funcs in mapping:
            if '{' not in path:
                self.mapping_dict[path] = (klass, funcs, [])
                continue
            prefix = prefix_str(path)
            # TODO 문자열 정규형 추가
            # int 정규형
            rexp_path = re.sub('\{\w*:int\}', '\d*', path)
            rexp = re.compile(rexp_path)
            self.mapping_list.append((prefix, rexp, path, klass, funcs))

    def lookup(self, req_method, req_path):
        t = self.mapping_dict.get(req_path)
        if t:
            klass, funcs, parms = t
            func = funcs.get(req_method)
            return klass, func, []

        for prefix, rexp, path, klass, funcs in self.mapping_list:
            if not req_path.startswith(prefix):
                continue
            m = rexp.match(req_path)
            if m:
                print(m)
                parms = [int(v) for v in m.groups()]
                print(parms)
                func = funcs.get(req_method)
                return klass, func, parms

        return None, None, None


if __name__ == '__main__':

    from apis.books import BooksAPI
    from apis.orders import OrdersApi

    # path, class, {method: func,}
    mapping_list = [

        (r"/api/books/", BooksAPI, {"GET": BooksAPI.do_index, "POST": BooksAPI.do_create}),
        (r"/api/books/{id:int}/", BooksAPI, {"GET": BooksAPI.do_index, "PUT": BooksAPI.do_create}),
        (r"/api/orders/", OrdersApi, {"GET": OrdersApi.do_show, "POST": OrdersApi.do_update})
    ]

    router = Router(mapping_list)
    assert router.lookup("GET", "/api/books/") == (BooksAPI, BooksAPI.do_index, [])
    assert router.lookup("POST", "/api/books/") == (BooksAPI, BooksAPI.do_create, [])
    print(router.lookup("PUT", "/api/books/123/"))
    # assert router.lookup("GET", "/api/books/123/") == (BooksAPI, BooksAPI.do_index, [123])

    # assert router.lookup("GET", "/api/books/23/test/") == (None, None, None)
