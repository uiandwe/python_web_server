# -*- coding: utf-8 -*-
import selectors

from http_handler import HTTPStatus
from logger import Logger
from parser.parser import ParserHttp
from router.router import StaticHandler
from urls import router
from utils import args_to_str, string_to_byte
from utils.decorator.memoization import LRU

LOG = Logger().log

responses_code = {
    v.value: (v.phrase, v.description) for v in HTTPStatus.__members__.values()
}

__all__ = (
    'Handle', 'RequestHandler', 'ResponseHandler'
)

default_headers = [('Accept-Charset', 'utf-8')]


class ServerError(Exception):
    __slots__ = ['msg']

    def __init__(self, msg='server error'):
        self.msg = msg

    def __str__(self):
        return self.msg


# TODO 상황별 http code 로직 추가


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

        # only HTTP or 1.0 이하는 에러
        if self.request is None or not self.request.protocol.startswith("HTTP/") or \
                self.request.version < ('1', '0'):
            res_data = ResponseHandler(self.request.protocol, 400, default_headers, '')()
            self.send(res_data)
            self.request = None

        # TODO body 확인

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

    def write(self):

        request_handler = None
        if self.request and self.request.method and self.request.url:
            try:
                if self.request.url.startswith("/static/"):
                    request_handler = (StaticHandler.do_index, [])
                else:
                    request_handler = router.lookup(self.request.method, self.request.url)
            except Exception as e:
                LOG.info(e)

        if request_handler:
            self.request.handler = request_handler
            self._write(self.request)
        else:
            self.close()

    def _write(self, request):

        if self._recv_buffer and request.handler is not (None, None):
            ret_data = ''
            try:
                ret_data = self.get_response_data(request)
            except Exception as e:
                LOG.error(e)

            if len(ret_data) > 0:
                code = 200
            else:
                code = 404

            response_data = ResponseHandler(request.protocol, code, default_headers, ret_data)()

            LOG.info(response_data)

            self.send(response_data)

            self.close()

    @LRU()
    def get_response_data(self, request):
        ret_data = ''
        api_handler, params = request.handler
        if api_handler:
            try:
                # self.request 를 넣을지 않넣을지 판단하기
                ret_data = api_handler(request)

                if ret_data is None:
                    raise ServerError

            # TODO 500 error 추가
            except Exception as e:
                LOG.error(e)

        return ret_data

    def send(self, send_data):
        try:
            self.sock.send(string_to_byte(send_data))
        except BlockingIOError:
            pass
        except Exception as e:
            LOG.error(e)

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
    __slots__ = ["method", "url", "protocol", "version", "params", "headers", "body", "handler", "content_type"]

    def __init__(self, request_line, request_headers):
        self.method = request_line['method']
        self.url = request_line['url']
        self.protocol = request_line['protocol']
        self.version = request_line['version']
        self.params = request_line['params']
        self.headers = request_headers
        self.body = None
        self.handler = None
        self.content_type = request_line['content_type']

    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.__class__, self.method, self.url, self.protocol, self.version, self.params)


class ResponseHandler:

    __slots__ = ["code", "message", "protocol", "headers_buffer", "body"]

    def __init__(self, protocol, code, headers, body):
        self.code = code
        self.message = responses_code[code][0]
        self.protocol = protocol
        self.headers_buffer = self.set_headers(headers)
        self.body = '' if body is None else body

    def __call__(self, *args, **kwargs):
        self.end_headers()

        _wfile = "{} {} {}".format(self.protocol, self.code, self.message)
        _wfile += "\r\n"
        _wfile += "".join(self.headers_buffer)

        if len(self.body) > 0:
            _wfile += "{}\r\n".format(self.body)
        return _wfile

    def end_headers(self):
        self.headers_buffer.append("\r\n")

    def set_headers(self, headers):
        headers_buffer = []

        for keyword, value in headers:
            headers_buffer.append(("%s: %s\r\n" % (keyword, value)))
        return headers_buffer
