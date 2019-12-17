# -*- coding: utf-8 -*-
"""
https://docs.python.org/3/howto/logging-cookbook.html
https://docs.python.org/ko/3/library/logging.handlers.html
"""

import logging
from logging.handlers import RotatingFileHandler

__all__ = (
    'Logger'
)


class Logger:
    __slots__ = ["mylogger"]

    def __init__(self):

        self.mylogger = logging.getLogger("my")
        self.mylogger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')

        stream_hander = logging.StreamHandler()
        stream_hander.setFormatter(formatter)

        log_max_size = 10 * 1024 * 1024
        log_file_count = 1
        file_handler = RotatingFileHandler(filename='./server.log',
                                           maxBytes=log_max_size,
                                           backupCount=log_file_count)
        file_handler.setFormatter(formatter)

        self.mylogger.addHandler(file_handler)
        self.mylogger.addHandler(stream_hander)

    def __call__(self, *args, **kwargs):
        return self.mylogger
