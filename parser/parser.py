# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from email._policybase import compat32
from email.parser import FeedParser
from io import StringIO

from http_handler import HTTPContentType
from logger import Logger

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
    def parser_request(self, request_line: str) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def parser_headers(self, request_headers: str) -> list:
        raise NotImplementedError()

    @abstractmethod
    def parser_url_params(self, params_arr: list) -> dict:
        raise NotImplementedError()


class ParserHttp(ParserImp):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        req_line, headers_alone = args[0].split(b'\r\n', 1)

        req_line = self.parser_request(req_line)

        request_headers = self.parser_headers(headers_alone)

        return req_line, request_headers

    def parser_request(self,
                       req_data: bytes) -> dict:
        """
        method, url, http protocol, http version, url params,  파서
        ex data) 'GET /static/css/main.css?file_version=1 HTTP/1.1'
        """

        req_infos = req_data.decode('utf-8').split(' ')

        method, urls, protocol, base_version_num, version_num = self.get_req_infos(req_infos)

        url_params = []
        origin_url = urls[0]

        file_type = origin_url.split("/")[-1]
        content_type = self.find_file_type(file_type)

        if len(urls) > 1:
            url_params = self.parser_url_params(urls[1:])

        return {"method": method,
                "url": origin_url,
                "protocol": protocol,
                "version": version_num,
                "params": url_params,
                'content_type': content_type}

    def get_req_infos(self, req_infos: list) -> tuple:
        method = req_infos[0]
        urls = req_infos[1].split('?')
        protocol = req_infos[2]
        base_version_num = protocol.split('/', 1)[1]
        version_num = tuple(base_version_num.split("."))

        return method, urls, protocol, base_version_num, version_num

    def find_file_type(self, file_type: str) -> str:
        if file_type and file_type.find(".") > 0:
            file_type = file_type.split(".")[-1]
            return response_content_type[file_type.upper()]
        return response_content_type['HTML']

    def parser_url_params(self,
                          params_arr: list) -> dict:
        """
        url 파라미터 파서
        """
        params_dict = {}
        if len(params_arr) > 0:
            for param in params_arr:
                param_split = param.split("=")
                params_dict[param_split[0]] = param_split[1]
        return params_dict

    def parser_headers(self,
                       request_headers: str) -> list:
        """
        헤더 파서
        """
        text = request_headers.decode('ASCII', errors='surrogateescape')
        fp = StringIO(text)
        feed_parser = FeedParser(None, policy=compat32)
        while True:
            data = fp.read(8192)
            if not data:
                break
            feed_parser.feed(data)
        return feed_parser.close()
