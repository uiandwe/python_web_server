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
    __slots__ = ["mylogger"]

    def __init__(self):

        self.create_log_folder("logs")

        self.mylogger = logging.getLogger("my")
        self.mylogger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        time_log_handler = TimedRotatingFileHandler(filename='./logs/server.log', when='midnight', interval=1,
                                                    encoding='utf-8')
        time_log_handler.setFormatter(formatter)
        time_log_handler.suffix = "%Y%m%d"

        self.mylogger.addHandler(time_log_handler)
        self.mylogger.addHandler(stream_handler)

    def __call__(self, *args, **kwargs):
        return self.mylogger

    def create_log_folder(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
