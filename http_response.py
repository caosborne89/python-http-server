import datetime
import mimetypes
import re

class HTTPResponse():
    def __init__(self, webroot, path):
        self.file_path = self.set_file_path(webroot, path)
        self.status = "500 Internal Server Error"

    def set_file_path(self, webroot, path):
        file_path = webroot + path

        if re.match(r'^(?!.*\.\w+$).*', file_path):
            if path[-1] == '/':
                return file_path + "index.html"
            return file_path + "/index.html"
        return file_path

    def get_raw_response(self):
        resource_data = self.get_resource()
        response_headers = self.get_response_headers(len(resource_data))

        return response_headers + resource_data

    def get_resource(self):
        file_data = bytes()

        try:
            with open(self.file_path, "rb") as file:
                file_data = file.read()
                self.status = "200 OK"
        except EOFError:
            exit()
        except FileNotFoundError:
            self.status = "404"
            file_data = b'<!DOCTYPE html><html><head><title>404 Not Found</title></head><body><h1>Not Found</h1><p>The requested URL was not found on this server.</p></body></html>'
            print("Couldn't find file")
        except:
            print("Unexpected error")

        return file_data

    def get_response_headers(self, resource_len):
        curr_time = datetime.datetime.now()

        curr_timestamp = curr_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        mimetype, _ = mimetypes.guess_type(self.file_path)
        content_type = mimetype

        if content_type == "text/html" or self.status == '404':
            content_type = f"{content_type}; charset=UTF-8"

        response_headers = bytes()
        response_headers += b'HTTP/1.1 ' + self.status.encode() + b'\r\n'
        response_headers += b'Date: ' + curr_timestamp.encode() + b'\r\n'
        response_headers += b'Server: AndysServer\r\n'

        if self.status == "200 OK" or self.status == '404':
            response_headers += b'Content-Type: ' + content_type.encode() + b'\r\n'
            response_headers += b'Content-Length: ' + str(resource_len).encode() + b'\r\n'

        response_headers += b'\r\n'
        return response_headers