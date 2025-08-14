import datetime
import mimetypes
import re

class HTTPResponse():
    def __init__(self, webroot, status=None, path=None, html=None):
        self.file_path = self.set_file_path(webroot, path)
        self.status = "500 Internal Server Error"
        self.html = html
        self.status = status

    def set_file_path(self, webroot, path):
        if not path:
            return None
        file_path = bytes(webroot, "utf-8") + path

        if re.match(b'^(?!.*\\.\\w+$).*', file_path):
            if path[-1] == '/':
                return file_path + b'index.html'
            return file_path + b'/index.html'
        return file_path

    def get_raw_response(self):
        resource_data = self.get_resource()
        response_headers = self.get_response_headers(len(resource_data))

        return response_headers + resource_data

    def get_resource(self):
        if self.html:
            return self.html

        file_data = bytes()

        try:
            with open(self.file_path, "rb") as file:
                file_data = file.read()
                self.status = b'200 OK'
        except EOFError:
            exit()
        except FileNotFoundError:
            self.status = b'404'
            file_data = b'<!DOCTYPE html><html><head><title>404 Not Found</title></head><body><h1>Not Found</h1><p>The requested URL was not found on this server.</p></body></html>'
            print("Couldn't find file")
        except:
            print("Unexpected error")

        return file_data

    def get_response_headers(self, resource_len):
        curr_time = datetime.datetime.now()

        curr_timestamp = curr_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        if self.file_path:
            mimetype, _ = mimetypes.guess_type(self.file_path)
            content_type = mimetype
        
        if not self.file_path or content_type == "text/html" or self.status == '404':
            content_type = f"text/html; charset=UTF-8"

        response_headers = bytes()
        response_headers += b'HTTP/1.1 ' + self.status + b'\r\n'
        response_headers += b'Date: ' + curr_timestamp.encode() + b'\r\n'
        response_headers += b'Server: AndysServer\r\n'

        response_headers += b'Content-Type: ' + content_type.encode() + b'\r\n'
        response_headers += b'Content-Length: ' + str(resource_len).encode() + b'\r\n'

        response_headers += b'\r\n'
        return response_headers