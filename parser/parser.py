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
    def parser_body(self):
        raise NotImplementedError()


class ParserHttp(ParserImp):

    def __init__(self, *args, **kwargs):
        super(ParserImp, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        req_line, headers_alone = args[0].split(b'\r\n', 1)

        req_line = self.parser_request(req_line)

        request_headers = self.parser_headers(headers_alone)
        LOG.info(request_headers)
        return req_line, request_headers

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

    def parser_headers(self, request_headers):
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
