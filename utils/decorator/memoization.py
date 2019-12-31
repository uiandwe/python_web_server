# -*- coding: utf-8 -*-
from functools import wraps, partial
from collections import Hashable


class Memoized:
    """Decorator.
    Caches a function's return value.
    """

    __slots__ = ["func", "cache"]

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        if not isinstance(args, Hashable):
            return self.func(*args)

        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        return self.func.__doc__

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


def memoize(func):
    cache = {}

    @wraps(func)
    def momoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return momoizer
