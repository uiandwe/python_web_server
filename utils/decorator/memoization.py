# -*- coding: utf-8 -*-
from functools import wraps, partial
from collections import Hashable


__all__ = (
    "LRU",
    "Memoized",
    "memoize"
)

# TODO cache_size 에러 체크


class LRU:
    """Decorator
    Least Recently Used (LRU)
    """
    __slots__ = ["func", "cache_list", "cache_dict", "cache_size"]

    def __init__(self, cache_size=128):
        self.cache_dict = {}
        self.cache_list = []
        self.cache_size = cache_size

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if not isinstance(args, Hashable):
                return func(*args)

            key = str(args) + str(kwargs)

            if key in self.cache_list:
                self.cache_list.remove(key)
                self.cache_list.append(key)
            elif self.cache_size > 0:
                if len(self.cache_list) == self.cache_size:
                    del self.cache_list[0]
                    del self.cache_dict[key]
                self.cache_list.append(key)
                self.cache_dict[key] = func(*args, **kwargs)
            else:
                self.cache_list.append(key)
                self.cache_dict[key] = func(*args, **kwargs)

            return self.cache_dict[key]

        return wrapper

    def __repr__(self):
        return self.func.__doc__

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


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
