# -*- coding: utf-8 -*-
import selectors

from logger import Logger
from utils import args_to_str, string_to_byte
from parser.parser import ParserHttp
from urls import router
from http import HTTPStatus

LOG = Logger.instance().log

responses = {
    v._value_: (v.phrase, v.description) for v in HTTPStatus.__members__.values()
}

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

        # only HTTP
        if self.request is None or not self.request.protocol.startswith("HTTP/"):
            return

        # 1.0 이하는 에러
        if self.request.version < ('1', '0'):
            return

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
                request_handler = router.lookup(self.request.method, self.request.url)
            except Exception as e:
                LOG.info(e)

        if request_handler:
            self._write(request_handler)
        else:
            self.close()

    def _write(self, request_handler):

        # TODO send 함수 만들기 (헤더 자동 만들기 함수)
        # TODO request_handler == (None, None) 일때 404 에러 반환
        if self._recv_buffer:
            ret_data = ''

            try:
                ret_data = request_handler[0](self.request)
            except Exception as e:
                LOG.error(e)

            code = 200
            headers = [('Content-Type', 'text/html'), ('Accept-Charset', 'utf-8')]
            response_data = ResponseHandler(self.request.protocol, code, headers, ret_data)()
            LOG.info(response_data)

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
    __slots__ = ["method", "url", "protocol", "version", "params", "headers", "body"]

    def __init__(self, request_line, request_headers):
        self.method = request_line['method']
        self.url = request_line['url']
        self.protocol = request_line['protocol']
        self.version = request_line['version']
        self.params = request_line['params']
        self.headers = request_headers
        self.body = None

    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.__class__, self.method, self.url, self.protocol, self.version, self.params)


class ResponseHandler:

    __slots__ = ["code", "message", "protocol", "headers_buffer", "body"]

    def __init__(self, protocol, code, headers, body):
        self.code = code
        self.message = responses[code][0]
        self.protocol = protocol
        self.headers_buffer = self.set_headers(headers)
        self.body = body

    def __call__(self, *args, **kwargs):
        self.end_headers()

        _wfile = "{} {} {}".format(self.protocol, self.code, self.message)
        _wfile += "\r\n"
        _wfile += "".join(self.headers_buffer)
        _wfile += "{}\r\n".format(self.body)
        return _wfile

    def end_headers(self):
        self.headers_buffer.append("\r\n")
        # self.flush_headers()

    def send_response_only(self, code, message=None):
        """Send the response header only."""
        if self.request_version != 'HTTP/0.9':
            if message is None:
                if code in self.responses:
                    message = self.responses[code][0]
                else:
                    message = ''
            if not hasattr(self, '_headers_buffer'):
                self._headers_buffer = []
            self._headers_buffer.append(("%s %d %s\r\n" %
                    (self.protocol_version, code, message)).encode(
                        'latin-1', 'strict'))

    def set_headers(self, headers):
        headers_buffer = []

        for keyword, value in headers:
            # headers_buffer.append(("%s: %s\r\n" % (keyword, value)).encode('latin-1', 'strict'))
            headers_buffer.append(("%s: %s\r\n" % (keyword, value)))
        return headers_buffer

    def flush_headers(self):
        if hasattr(self, '_headers_buffer'):
            self.wfile.write(b"".join(self.headers_buffer))
            self.headers_buffer = []


class RenderHandler:
    def __init__(self):
        pass

