# -*- coding: utf-8 -*-

__all__ = (
    'args_to_str'
)


def args_to_str(*args):
    return ''.join(tuple(map(str, args)))
