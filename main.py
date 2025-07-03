import socket
from http_request import HTTPRequest
from http_response import HTTPResponse
import datetime
import mimetypes
import sys

def open_conn():
    HOST = ""
    PORT = 8080
    WEB_ROOT = "./www"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # setsockopt must be called before s.bind
        # socket.SO_REUSEADDR will keep the address and port free  after the program exits
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                req = HTTPRequest(data.decode("utf-8"))
                conn.sendall(HTTPResponse(WEB_ROOT, req.get_path()).get_raw_response())

def main():
    print("Listening on localhost:8080...")
    # Without this while loop, the socket will close when the use closes their browser
    # and the program will end.
    while True:
        try:
            open_conn()
        except KeyboardInterrupt:
            break
    sys.exit()

if __name__ == "__main__":
    main()