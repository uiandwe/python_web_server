# -*- coding: utf-8 -*-
# TODO 클래스화
# TODO slot

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print("accepted connection from ", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    # 클라에서 데이터 받기
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print("closeing conn to ", data.addr)
            sel.unregister(sock)
            sock.close()

    # 클라에 데이터 보내기
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("echo ", repr(data.outb), "to", data.addr)
            # sent = sock.send(data.outb)
            # data.outb = data.outb[sent:]
            sock.send(b"HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body>Hello World</body></html>\n")
            print("closeing conn to ", data.addr)
            sel.unregister(sock)
            sock.close()


host, port = "127.0.0.1", 65432
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listion on ", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=10)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)

except KeyboardInterrupt:
    pass
finally:
    sel.close()

