# -*- coding: utf-8 -*-
# https://www.slideshare.net/kwatch/how-to-make-the-fastest-router-in-python

class Router:
    __slots__ = ["mapping"]

    def __init__(self, mapping):
        self.mapping = mapping

    def lookup(self, method, url):
        print(method, url)

        return ()



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
