# -*- coding: utf-8 -*-
from email._policybase import compat32
from email.parser import FeedParser
from io import StringIO

from abc import ABCMeta, abstractmethod
from logger import Logger
from http_handler import HTTPContentType

LOG = Logger().log

response_content_type = {
    v.name: v.value for v in HTTPContentType.__members__.values()
}

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

        return req_line, request_headers

    def parser_request(self, request_line: str) -> dict:
        """
        method, url, http protocol, http version, url params,  파서
        :return:
        """
        req_line_arr = request_line.split(b' ')

        method = req_line_arr[0].decode('utf-8')

        url_split = req_line_arr[1].decode('utf-8').split('?')

        protocol = req_line_arr[2].decode('utf-8')
        base_version_number = protocol.split('/', 1)[1]
        version_number = tuple(base_version_number.split("."))

        url_params = []
        origin_url = url_split[0]

        req_file_type = origin_url.split("/")[-1]
        content_type = HTTPContentType['HTML']

        if req_file_type and req_file_type.find(".") > 0:
            file_type = req_file_type.split(".")[-1]
            content_type = HTTPContentType[file_type.upper()]

        if len(url_split) > 1:
            url_params = self.parser_url_params(url_split[1:])

        return {"method": method,
                "url": origin_url,
                "protocol": protocol,
                "version": version_number,
                "params": url_params,
                'content_type': content_type}

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
