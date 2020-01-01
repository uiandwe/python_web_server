# -*- coding: utf-8 -*-
import os
import sys
import types

# TODO 해당 구문 쉽게 쓸수 있는지 확인하기
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from apis.books import BooksAPI
from apis.homes import HomesAPI
from apis.orders import OrdersApi
from router.router import Router


mapping_list = [
	# path, {method: func,}
	(r"/", {"GET": HomesAPI.do_index, "POST": HomesAPI.do_create}),
	(r"/api/books/", {"GET": BooksAPI.do_index, "POST": BooksAPI.do_create}),
	(r"/api/books/{id:int}/", {"GET": BooksAPI.do_index, "PUT": BooksAPI.do_create}),
	(r"/api/orders/", {"GET": OrdersApi.do_show, "POST": OrdersApi.do_update})
]

router = Router(mapping_list)
router2 = Router(mapping_list)


def test_router_singleton():
	assert id(router) == id(router2)


def test_router_lookup():
	assert router.lookup("GET", "/") == (HomesAPI.do_index, [])
	assert router.lookup("GET", "/api/books/") == (BooksAPI.do_index, [])
	assert router.lookup("POST", "/api/books/") == (BooksAPI.do_create, [])
	assert router.lookup("GET", "/api/orders/") == (OrdersApi.do_show, [])
	assert router.lookup("POST", "/api/orders/") == (OrdersApi.do_update, [])
	assert router.lookup("GET", "/api/books/123/") == (BooksAPI.do_index, [types.SimpleNamespace(name='id', type='int', data='123')])
	assert router.lookup("GET", "/api/books/23/test/") == (None, None)
