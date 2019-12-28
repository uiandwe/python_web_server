# -*- coding: utf-8 -*-
# TODO http 호환 클래스 ( http 상태 코드 선언)
# -----------------------------------------------------
# TODO http method 구현하기
# TODO 미들웨어 구현하기
# TODO file read view 구현하기 (html)
# TODO static 구현
# -----------------------------------------------------
# TODO 클래스 이름 바꾸기
# TODO type 지정하기 (from typing import Dict, Tuple, Union, Iterator, Sequence, List)
# TODO test 로직 추가 하기
# TODO string to byte 함수 추가
# TODO wsgi 호환
# TODO weakref 객체 확인하기
# TODO 초기 파라미터 셋팅
# TODO CORS 구현
# TODO http2 적용

from web_server import WebServer
from logger import Logger

LOG = Logger.instance().log

if __name__ == '__main__':
    LOG.info("server start!!!")

    WebServer()()
