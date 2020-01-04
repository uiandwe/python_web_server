# -*- coding: utf-8 -*-
import os

__all__ = (
    'args_to_str',
    'string_to_byte',
    'byte_to_string',
    'create_folder'
)


def args_to_str(*args) -> str:
    return ''.join(tuple(map(str, args)))


def string_to_byte(s: str) -> bytes:
    return str.encode(s)


def byte_to_string(b: bytes) -> str:
    return str(b)


def create_folder(dir_name: str):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
