# -*- coding: utf-8 -*-
from apis.books import BooksAPI
from apis.orders import OrdersApi
from apis.homes import HomesAPI
from router import Router

__all__ = (
    'router'
)

mapping_list = [
    (r"/", {"GET": HomesAPI.do_index, "POST": HomesAPI.do_create}),
    (r"/api/books/", {"GET": BooksAPI.do_index, "POST": BooksAPI.do_create}),
    (r"/api/books/{id:int}/", {"GET": BooksAPI.do_index, "PUT": BooksAPI.do_create}),
    (r"/api/orders/", {"GET": OrdersApi.do_show, "POST": OrdersApi.do_update})
]

router = Router(mapping_list)
