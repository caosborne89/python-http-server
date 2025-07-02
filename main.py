import socket
from http_request import HTTPRequest
from http_response import HTTPResponse
import datetime
import mimetypes

def open_conn():
    HOST = ""
    PORT = 8080
    WEB_ROOT = "./www"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
    while True:
        open_conn()

if __name__ == "__main__":
    main()