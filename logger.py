# -*- coding: utf-8 -*-
"""
https://docs.python.org/3/howto/logging-cookbook.html
https://docs.python.org/ko/3/library/logging.handlers.html
"""

# TODO logging.ini 파일로 설정 대체

import os
import logging
from logging.handlers import TimedRotatingFileHandler

__all__ = (
    'Logger'
)


class Logger:
    __slots__ = ["_mylogger"]
    __instance = None

    def __init__(self):

        self.create_log_folder("logs")

        self._mylogger = logging.getLogger("my")
        self._mylogger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        time_log_handler = TimedRotatingFileHandler(filename='./logs/server.log', when='midnight', interval=1,
                                                    encoding='utf-8')
        time_log_handler.setFormatter(formatter)
        time_log_handler.suffix = "%Y%m%d"

        self._mylogger.addHandler(time_log_handler)
        self._mylogger.addHandler(stream_handler)

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

    @property
    def mylogger(self):
        return self._mylogger

    def create_log_folder(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
