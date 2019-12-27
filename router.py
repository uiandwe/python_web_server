# -*- coding: utf-8 -*-
# https://www.slideshare.net/kwatch/how-to-make-the-fastest-router-in-python

import re
import types


def prefix_str(s):
    return s.split('{', 1)[0]


def replace_rexp(path):
    # int 정규형
    rexp = re.sub('\{\w*:int\}', '\d*', path)
    # str 정규형
    rexp = re.sub('\{\w*:str\}', '\w*', rexp)
    rexp = re.compile(rexp)

    return rexp

# TODO func 빼기
# TODO 변수 이름 바꾸기
#
class Router:
    def __init__(self, mapping):
        self.mapping_list = []
        self.mapping_dict = {}
        for path, funcs in mapping:
            if '{' not in path:
                self.mapping_dict[path] = (funcs, [])
                continue

            prefix = prefix_str(path)

            rexp = replace_rexp(path)

            self.mapping_list.append((prefix, rexp, path, funcs))

    def lookup(self, req_method, req_path):
        t = self.mapping_dict.get(req_path)
        if t:
            funcs, parms = t
            func = funcs.get(req_method)
            return func, []

        for prefix, rexp, path, funcs in self.mapping_list:
            if not req_path.startswith(prefix):
                continue
            m = rexp.match(req_path)
            if m:
                parms = []
                path_split = path.split("/")
                req_split = req_path.split("/")
                if len(path_split) != len(req_split):
                    continue

                for origin_data, req_data in zip(path_split, req_split):
                    if origin_data == req_data:
                        continue
                    temp = re.search('\{(\w*):(\w*)\}', origin_data).groups()
                    data = types.SimpleNamespace(name=temp[0], type=temp[1], data=req_data)
                    parms.append(data)
                func = funcs.get(req_method)
                return func, parms

        return None, None, None


if __name__ == '__main__':

    from apis.books import BooksAPI
    from apis.orders import OrdersApi

    # path, class, {method: func,}
    mapping_list = [

        (r"/api/books/", {"GET": BooksAPI.do_index, "POST": BooksAPI.do_create}),
        (r"/api/books/{id:int}/", {"GET": BooksAPI.do_index, "PUT": BooksAPI.do_create}),
        (r"/api/orders/", {"GET": OrdersApi.do_show, "POST": OrdersApi.do_update})
    ]

    router = Router(mapping_list)
    assert router.lookup("GET", "/api/books/") == (BooksAPI.do_index, [])
    assert router.lookup("POST", "/api/books/") == (BooksAPI.do_create, [])
    assert router.lookup("GET", "/api/orders/") == (OrdersApi.do_show, [])
    assert router.lookup("POST", "/api/orders/") == (OrdersApi.do_update, [])
    assert router.lookup("GET", "/api/books/123/") == (BooksAPI.do_index,
                                                       [types.SimpleNamespace(name='id', type='int', data='123')])
    assert router.lookup("GET", "/api/books/23/test/") == (None, None, None)
