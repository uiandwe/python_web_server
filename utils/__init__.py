# -*- coding: utf-8 -*-
import os

__all__ = (
    'args_to_str',
    'string_to_byte',
    'byte_to_string',
    'create_folder'
)


def args_to_str(*args) -> str:
    """

    :param args:
    :return:
    """
    return ''.join(tuple(map(str, args)))


def string_to_byte(s) -> bytes:
    """

    :param s:
    :return:
    """
    return str.encode(s)


def byte_to_string(b) -> str:
    """

    :param b:
    :return:
    """
    return str(b)


def create_folder(dir_name: str):
    """

    :param dir_name:
    :return:
    """
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
