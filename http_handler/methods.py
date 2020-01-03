# -*- coding: utf-8 -*-
import inspect
from typing import List


class Methods:
    @classmethod
    def do_options(cls, req) -> List:
        return inspect.getmembers(cls, predicate=inspect.ismethod)

    @staticmethod
    def do_head(req) -> str:
        return ''
