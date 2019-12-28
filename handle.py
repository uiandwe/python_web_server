# -*- coding: utf-8 -*-
import selectors

from logger import Logger
from utils import args_to_str, string_to_byte
from parser.parser import ParserHttp
from urls import router

LOG = Logger.instance().log

__all__ = (
    'Handle', 'Request'
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
        request_handler = None
        if self.request and self.request.method and self.request.url:
            try:
                request_handler = router.lookup(self.request.method.decode('utf-8'), self.request.url.decode('utf-8'))
            except Exception as e:
                LOG.info(e)

        self._write(request_handler)

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
        # TODO 경로가 없는 None 일 경우 처리하기 ( handle.py - 86 - ERROR - 'NoneType' object is not callable )

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

