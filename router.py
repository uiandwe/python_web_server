# -*- coding: utf-8 -*-
# https://www.slideshare.net/kwatch/how-to-make-the-fastest-router-in-python
import re
import types
from singleton import Singleton


def prefix_str(s):
    return s.split('{', 1)[0]


def replace_rexp(path):
    # int 정규형
    rexp = re.sub('\{\w*:int\}', '\d*', path)
    # str 정규형
    rexp = re.sub('\{\w*:str\}', '\w*', rexp)
    rexp = re.compile(rexp)

    return rexp

# TODO 변수 이름 바꾸기
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

            rexp = replace_rexp(path)

            self.mapping_list.append((prefix, rexp, path, funcs))

    def lookup(self, req_method, req_path):
        t = self.mapping_dict.get(req_path)
        if t:
            funcs, parms = t
            func = funcs.get(req_method)
            return func, []

        for prefix, rexp, path, funcs in self.mapping_list:
            if not req_path.startswith(prefix):
                continue
            m = rexp.match(req_path)
            if m:
                parms = []
                path_split = path.split("/")
                req_split = req_path.split("/")
                if len(path_split) != len(req_split):
                    continue

                for origin_data, req_data in zip(path_split, req_split):
                    if origin_data == req_data:
                        continue
                    temp = re.search('\{(\w*):(\w*)\}', origin_data).groups()
                    data = types.SimpleNamespace(name=temp[0], type=temp[1], data=req_data)
                    parms.append(data)
                func = funcs.get(req_method)
                return func, parms

        return None, None, None
