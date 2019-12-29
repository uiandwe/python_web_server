# -*- coding: utf-8 -*-
import selectors

from logger import Logger
from utils import args_to_str, string_to_byte
from parser.parser import ParserHttp
from urls import router
from http import HTTPStatus

LOG = Logger.instance().log

__all__ = (
    'Handle', 'RequestHandler', 'ResponseHandler'
)
# TODO http status code -> init.py


class Handle:

    __slots__ = ["selector", "sock", "addr", "_recv_buffer", "_send_buffer", "_json_header_len", "request"]

    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._json_header_len = None
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
            self.request = RequestHandler(req_line, request_headers)
            LOG.info(self.request)

        # TODO 다른 프로토콜도 가능하도록 설계하기
        if self.request is None or self.request.protocol in [b'http/1.1']:
            return

        # TODO body 확인

    def write(self):
        request_handler = None
        if self.request and self.request.method and self.request.url:
            try:
                request_handler = router.lookup(self.request.method, self.request.url)
            except Exception as e:
                LOG.info(e)

        if request_handler:
            self._write(request_handler)
        else:
            self.close()

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

    def _write(self, request_handler):

        # TODO send 함수 만들기 (헤더 자동 만들기 함수)
        # TODO request_handler == (None, None) 일때 404 에러 반환
        if self._recv_buffer:
            ret_data = ''

            try:
                ret_data = request_handler[0](self.request)
            except Exception as e:
                LOG.error(e)
            LOG.info(args_to_str(type(string_to_byte(ret_data)), string_to_byte(ret_data)))

            response_data = "HTTP/1.1 200 OK\nContent-Type: text/html\nAccept-Charset: utf-8\n\n{}\n".format(ret_data)
            try:
                self.sock.send(string_to_byte(response_data))
            except BlockingIOError:
                pass
            except Exception as e:
                LOG.error(e)

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


class RequestHandler:
    __slots__ = ["method", "url", "protocol", "params", "headers", "body"]

    def __init__(self, request_line, request_headers):
        self.method = request_line['method']
        self.url = request_line['url']
        self.protocol = request_line['protocol']
        self.params = request_line['params']
        self.headers = request_headers
        self.body = None

        responses = {
            v._value_: (v.phrase, v.description)
            for v in HTTPStatus.__members__.values()
        }

    def __repr__(self):
        return "{} {} {} {} {}".format(self.__class__, self.method, self.url, self.protocol, self.params)


class ResponseHandler:
    def __init__(self, request):
        self.error_code = None
        self.error_message = None
        self.command = None
        self.path = None
        self.request_version = None
        self.headers = None


class RenderHandler:
    def __init__(self):
        pass

