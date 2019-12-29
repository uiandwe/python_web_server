# -*- coding: utf-8 -*-
from email._policybase import compat32
from email.parser import FeedParser
from io import StringIO

from abc import ABCMeta, abstractmethod
from logger import Logger

LOG = Logger.instance().log

__all__ = (
    'ParserHttp'
)

class ParserImp:
    __metaclass__ = ABCMeta

    @abstractmethod
    def parser_request(self):
        raise NotImplementedError()

    @abstractmethod
    def parser_headers(self):
        raise NotImplementedError()

    @abstractmethod
    def parser_url_params(self):
        raise NotImplementedError()


class ParserHttp(ParserImp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        req_line, headers_alone = args[0].split(b'\r\n', 1)

        req_line = self.parser_request(req_line)

        request_headers = self.parser_headers(headers_alone)
        LOG.info(request_headers)
        return req_line, request_headers

    def parser_request(self, request_line: str) -> dict:
        """
        method, url, http protocol 파서
        :return:
        """
        req_line_arr = request_line.split(b' ')

        url_split = req_line_arr[1].decode('utf-8').split('?')

        url_params = []
        origin_url = url_split[0]

        if len(url_split) > 1:
            url_params = self.parser_url_params(url_split[1:])

        d = {"method": req_line_arr[0].decode('utf-8'),
             "url": origin_url,
             "protocol": req_line_arr[2].decode('utf-8'),
             'params': url_params}
        return d

    def parser_url_params(self, params_arr) -> dict:
        """
        url 파라미터 파서
        :param url:
        :return:
        """
        params_dict = {}
        if len(params_arr) > 0:
            for param in params_arr:
                param_split = param.split("=")
                params_dict[param_split[0]] = param_split[1]
        return params_dict

    def parser_headers(self, request_headers: str) -> list:
        """
        헤더 파서
        :return:
        """
        text = request_headers.decode('ASCII', errors='surrogateescape')
        fp = StringIO(text)
        feedparser = FeedParser(None, policy=compat32)
        while True:
            data = fp.read(8192)
            if not data:
                break
            feedparser.feed(data)
        return feedparser.close()
