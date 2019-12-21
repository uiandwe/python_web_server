# -*- coding: utf-8 -*-
import selectors
from logger import Logger
from utils import args_to_str


class Message:

    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""

        # ??? 로그 객체를 어떻게 관리 해야 하지???
        self.LOG = Logger.instance().log

    def _read(self):
        try:
            data = self.sock.recv(4096)
        except BlockingIOError:
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._recv_buffer:
            self.LOG.info(args_to_str("sending", repr(self._recv_buffer), "to", self.addr))
            try:
                # sent = self.sock.send(self._send_buffer)
                self.sock.send(b"HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body>Hello World</body></html>\n")
            except BlockingIOError:
                pass

            self.close()

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

    def write(self):
        self._write()

    def close(self):
        self.LOG.info(args_to_str("closing connection to", self.addr))
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            self.LOG.error(repr(e))

        try:
            self.sock.close()
        except OSError as e:
            self.LOG.error(repr(e))
        finally:
            self.sock = None
