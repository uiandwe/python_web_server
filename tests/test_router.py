# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from router import Router
import types

from apis.books import BooksAPI
from apis.orders import OrdersApi

mapping_list = [
	# path, {method: func,}
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
