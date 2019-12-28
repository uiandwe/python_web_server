# -*- coding: utf-8 -*-
# https://wikidocs.net/3693

__all__ = (
    'Singleton'
)


class Singleton(type):
    """
    상속용 싱글턴
    """
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class SingletonInheritance(type):
    """
    상속용 싱글턴 2
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonInheritance, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def singleton_decorator(class_):
    """
    데코레이터용 싱글턴, siaticMethod 접근 불가
    """
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance
