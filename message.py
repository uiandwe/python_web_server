# -*- coding: utf-8 -*-
import selectors
from logger import Logger
from utils import args_to_str
from email.parser import BytesParser

LOG = Logger.instance().log

__all__ = (
    'Message', 'Request'
)


class Message:

    __slots__ = ["selector", "sock", "addr", "_recv_buffer", "_send_buffer", "_json_header_len"]

    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._json_header_len = None

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self._recv_buffer:
            request = Parser()(self._recv_buffer)
            LOG.info(request)
        # TODO http 프로토콜 확인

        # TODO 헤더 확인

        # TODO 파라미터 확인

        # TODO body 확인

        #


    def write(self):
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


class Parser:
    def __call__(self, *args, **kwargs):
        req_line, headers_alone = args[0].split(b'\r\n', 1)

        req_line = self.parser_request(req_line)

        request_headers = self.parser_headers(headers_alone)

        return Request(req_line, request_headers)

    def parser_request(self, request_line):
        """
        method, url, http protocol 파서
        :return:
        """
        req_line_arr = request_line.split(b' ')
        d = {"method": req_line_arr[0],
             "url": req_line_arr[1],
             "protocol": req_line_arr[2]}
        return d

    # TODO BytesParser().parsebytes() 구현하기
    def parser_headers(self, request_headers):
        """
        헤더 파서
        :return:
        """
        return BytesParser().parsebytes(request_headers)

    # TODO parser_body
    def parser_body(self):
        pass


class Request:
    __slots__ = ["command", "url", "protocol", "headers", "body"]

    def __init__(self, request_line, request_headers):
        self.command = request_line['method']
        self.url = request_line['url']
        self.protocol = request_line['protocol']
        self.headers = request_headers
        self.body = None

    def __repr__(self):
        return "{} {} {} {}".format(self.__class__, self.command, self.url, self.protocol)


class Response:
    def __init__(self):
        self.error_code = None
        self.error_message = None
        self.command = None
        self.path = None
        self.request_version = None
        self.headers = None

