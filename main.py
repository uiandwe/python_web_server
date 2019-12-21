# -*- coding: utf-8 -*-
# TODO 클래스 이름 바꾸기
# TODO type 지정하기 (from typing import Dict, Tuple, Union, Iterator, Sequence, List)
# TODO test 로직 추가 하기
# TODO socket 클래스로 분리하기
# TODO string to byte 함수 추가
# TODO wsgi 호환
# TODO weakref 객체 확인하기
# TODO 초기 파라미터 셋팅
# TODO http 호환 클래스 ( http 상태 코드 선언)
# TODO 멀티스레딩
# TODO http method 구현하기
# TODO file read view 구현하기


import selectors
import socket
import types
from message import Message
from _thread import start_new_thread

from logger import Logger
from utils import args_to_str

LOG = None


class WebFrameWork:
    __slots__ = ["host", "port", "lsock", "sel"]

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 65432
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sel = selectors.DefaultSelector()

    def __call__(self, *args, **kwargs):
        self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lsock.bind((self.host, self.port))
        self.lsock.listen()
        LOG.info(args_to_str("listion on ", (self.host, self.port)))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = self.sel.select(timeout=10)
                for key, mask in events:
                    if key.data is None:
                        self.accept_handler(key.fileobj)
                    else:
                        message_obj = key.data
                        try:
                            message_obj.process_events(mask)
                        except Exception:
                            message_obj.close()
        except KeyboardInterrupt:
            LOG.info("close server ")
        finally:
            self.sel.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sel.close()

    def accept_handler(self, sock):
        conn, addr = sock.accept()
        LOG.info(args_to_str("accepted connection from ", addr))
        conn.setblocking(False)

        start_new_thread(self.thread_socket, (conn, addr))

    def thread_socket(self, conn, addr):
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message_obj = Message(self.sel, conn, addr)
        self.sel.register(conn, events, data=message_obj)


if __name__ == '__main__':
    LOG = Logger.instance().log
    LOG.info("server start!!!")

    WebFrameWork()()

