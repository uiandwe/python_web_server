# -*- coding: utf-8 -*-
import selectors
import socket
from _thread import start_new_thread

from logger import Logger
from handle import Handle
from utils import args_to_str

LOG = Logger().log

__all__ = (
    'WebServer'
)


class WebServer:
    __slots__ = ["host", "port", "lsock", "sel"]

    def __init__(self, host="127.0.0.1", port=65432):
        self.host = host
        self.port = port
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
                        handle_obj = key.data
                        try:
                            handle_obj.process_events(mask)
                        except Exception as e:
                            LOG.error(e)
                            handle_obj.close()
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
        handle_obj = Handle(self.sel, conn, addr)
        self.sel.register(conn, events, data=handle_obj)
