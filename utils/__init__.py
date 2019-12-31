# -*- coding: utf-8 -*-

__all__ = (
    'args_to_str', 'string_to_byte', 'byte_to_string'
)


def args_to_str(*args):
    return ''.join(tuple(map(str, args)))


def string_to_byte(s):
    return str.encode(s)


def byte_to_string(b):
    return str(b)
