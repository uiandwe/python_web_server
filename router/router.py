# -*- coding: utf-8 -*-
# https://www.slideshare.net/kwatch/how-to-make-the-fastest-router-in-python


import re
import types

from logger import Logger
from singleton import Singleton

LOG = Logger().log


__all__ = (
    'Router'
)


def prefix_str(s):
    return s.split('{', 1)[0]


def replace_params_rexp(path):

    # int 정규형
    replace_path = re.sub('\{\w*:int\}', '\d*', path)
    # str 정규형
    replace_path = re.sub('\{\w*:str\}', '\w*', replace_path)

    return re.compile(replace_path)


# TODO warrning 처리 하기


class Router(object, metaclass=Singleton):
    __slots__ = ["mapping_list", "mapping_dict"]

    def __init__(self, mapping):
        self.mapping_list = []
        self.mapping_dict = {}
        for path, funcs in mapping:
            if '{' not in path:
                self.mapping_dict[path] = (funcs, [])
                continue

            prefix = prefix_str(path)

            regx_path = replace_params_rexp(path)

            self.mapping_list.append((prefix, regx_path, path, funcs))

    def lookup(self, req_method, req_path):
        path_dict = self.mapping_dict.get(req_path)
        if path_dict:
            funcs, parms = path_dict
            func = funcs.get(req_method)
            return func, []

        for prefix, regx_path, path, funcs in self.mapping_list:
            if not req_path.startswith(prefix):
                continue

            path_match = regx_path.match(req_path)

            if path_match:
                parms = []
                path_split = path.split("/")
                req_path_split = req_path.split("/")

                if len(path_split) != len(req_path_split):
                    continue

                for origin_data, req_data in zip(path_split, req_path_split):
                    if origin_data == req_data:
                        continue
                    parse_path_parmas = re.search("\{(\w*):(\w*)\}", origin_data).groups()
                    data = types.SimpleNamespace(name=parse_path_parmas[0], type=parse_path_parmas[1], data=req_data)
                    parms.append(data)

                func = funcs.get(req_method)
                return func, parms

        return None, None, None
