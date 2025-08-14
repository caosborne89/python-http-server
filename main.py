import socket
from http_request import HTTPRequest
from http_response import HTTPResponse
import datetime
import mimetypes
import sys
import selectors

from http_error import HTTPError

HOST = ""
PORT = 8080
WEB_ROOT = "./www"


def open_conn():
    sel = selectors.DefaultSelector()

    def accept(sock, mask):
        conn, addr = s.accept()
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, read)

    def read(conn, mask):
        data = conn.recv(1024)
        if data:
            try:
                req = HTTPRequest(data)
                conn.send(HTTPResponse(WEB_ROOT, path=req.get_path()).get_raw_response())
            except HTTPError as e:
                conn.send(HTTPResponse(WEB_ROOT, status=e.status, html=e.response_html()).get_raw_response())

        else:
            sel.unregister(conn)
            conn.close()

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    s.setblocking(False)
    sel.register(s, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

def main():
    print(f"Listening on {HOST if HOST else "localhost"}:{PORT}...")

    try:
        open_conn()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()