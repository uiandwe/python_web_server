# -*- coding: utf-8 -*-
import selectors

from logger import Logger
from utils import args_to_str, byte_to_string
from parser.parser import ParserHttp
from urls import router

LOG = Logger.instance().log

__all__ = (
    'Message', 'Request'
)
# TODO http status code -> init.py

# TODO handle
class Message:

    __slots__ = ["selector", "sock", "addr", "_recv_buffer", "_send_buffer", "_json_header_len", "request"]

    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._json_header_len = None
        # TODO 미리 request로 선언해도 되는가?
        self.request = None

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self._recv_buffer:
            req_line, request_headers = ParserHttp()(self._recv_buffer)
            self.request = Request(req_line, request_headers)
            LOG.info(self.request)

        # TODO 다른 프로토콜도 가능하도록 설계하기
        if self.request is None or self.request.protocol in [b'http/1.1']:
            return

        # TODO 헤더 확인

        # TODO 파라미터 확인

        # TODO body 확인

    def write(self):

        # TODO send
        LOG.info(args_to_str("url ", self.request.url))
        LOG.info(args_to_str("method ", self.request.method))
        try:
            LOG.info(router.lookup(self.request.method, str(self.request.url)))
        except Exception as e:
            LOG.info(e)

        self._write()


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
            LOG.info(args_to_str("sending", repr(self._recv_buffer), "to", self.addr))
            try:
                # sent = self.sock.send(self._send_buffer)
                self.sock.send(b"HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body>Hello World</body></html>\n")
            except BlockingIOError:
                pass

            self.close()

    def close(self):
        LOG.info(args_to_str("closing connection to", self.addr))
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            LOG.error(repr(e))

        try:
            self.sock.close()
        except OSError as e:
            LOG.error(repr(e))
        finally:
            self.sock = None

# TODO RequestHandler
class Request:
    __slots__ = ["method", "url", "protocol", "headers", "body"]

    def __init__(self, request_line, request_headers):
        self.method = request_line['method']
        self.url = request_line['url']
        self.protocol = request_line['protocol']
        self.headers = request_headers
        self.body = None

    def __repr__(self):
        return "{} {} {} {}".format(self.__class__, self.method, self.url, self.protocol)

# TODO /Users/sj.hyeon/development/env/python36/lib/python3.6/site-packages/werkzeug/wrappers/base_response.py
class Response:
    def __init__(self):
        self.error_code = None
        self.error_message = None
        self.command = None
        self.path = None
        self.request_version = None
        self.headers = None

