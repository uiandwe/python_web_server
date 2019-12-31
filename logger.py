# -*- coding: utf-8 -*-
"""
https://docs.python.org/3/howto/logging-cookbook.html
https://docs.python.org/ko/3/library/logging.handlers.html
"""

# TODO logging.ini 파일로 설정 대체

import os
import logging
from utils.klass.singleton import Singleton
from logging.handlers import TimedRotatingFileHandler

__all__ = (
    'Logger'
)


class Logger(metaclass=Singleton):
    __slots__ = ["_log"]
    __instance = None

    def __init__(self):

        self.create_log_folder("logs")

        self._log = logging.getLogger("my")
        self._log.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        time_log_handler = TimedRotatingFileHandler(filename='./logs/server.log', when='midnight', interval=1,
                                                    encoding='utf-8')
        time_log_handler.setFormatter(formatter)
        time_log_handler.suffix = "%Y%m%d"

        self._log.addHandler(time_log_handler)
        self._log.addHandler(stream_handler)

    @property
    def log(self):
        return self._log

    @staticmethod
    def create_log_folder(dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
