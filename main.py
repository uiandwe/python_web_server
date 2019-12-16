# -*- coding: utf-8 -*-
# TODO logger 추가 하기
# TODO socket 클래스로 분리하기
# TODO string to byte 함수 추가
# TODO wsgi 호환
# 


import sys
import socket
import selectors
import types


class WebFrameWork:
    __slots__ = ["host", "port", "lsock", "sel"]

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 65432
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sel = selectors.DefaultSelector()

    def __call__(self, *args, **kwargs):
        self.lsock.bind((self.host, self.port))
        self.lsock.listen()
        print("listion on ", (self.host, self.port))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)


        while True:
            events = self.sel.select(timeout=10)
            for key, mask in events:
                if key.data is None:
                    self.accept_wrapper(key.fileobj)
                else:
                    self.service_connection(key, mask)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sel.close()


    def accept_wrapper(self, sock):
        conn, addr = sock.accept()
        print("accepted connection from ", addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data

        # 클라에서 데이터 받기
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data.outb += recv_data
            else:
                print("closeing conn to ", data.addr)
                self.sel.unregister(sock)
                sock.close()

        # 클라에 데이터 보내기
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print("echo ", repr(data.outb), "to", data.addr)
                # sent = sock.send(data.outb)
                # data.outb = data.outb[sent:]
                sock.send(b"HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body>Hello World</body></html>\n")
                print("closeing conn to ", data.addr)
                self.sel.unregister(sock)
                sock.close()


if __name__ == '__main__':
    wfw = WebFrameWork()
    wfw()
