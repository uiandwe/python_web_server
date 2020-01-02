# -*- coding: utf-8 -*-

# TODO type 지정하기 (from typing import Dict, Tuple, Union, Iterator, Sequence, List)
# TODO 미들웨어 구현하기
# TODO cache 구현
# -----------------------------------------------------
# TODO 폴더와 파일 레벨 맞추기
# TODO 클래스 이름 바꾸기
# TODO test 로직 추가 하기
# -----------------------------------------------------
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
