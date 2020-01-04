# -*- coding: utf-8 -*-

# TODO test 로직 추가 하기
# TODO .env 상수 적용하기
# TODO 미들웨어 구현하기
# TODO cache 구현
# -------------------- WAS ------------------------
# TODO http method 구현하기
# TODO wsgi 호환
# TODO weakref 객체 확인하기
# TODO 초기 파라미터 셋팅 (debug, log, template 등)
# TODO CORS 구현
# TODO http2 적용

from http_handler.web_server import WebServer
from logger import Logger

LOG = Logger().log

if __name__ == '__main__':
    LOG.info("server start!!!")

    WebServer()()
