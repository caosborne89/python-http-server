import re
class HTTPRequest():
    def __init__(self, data):
        self.set_properties(data)

    def set_properties(self, data):

        lines = re.split(r"\r\n|\r|\n", data)

        req_line = lines.pop(0)
        req_line = req_line.split(" ")
        self.http_method = req_line[0]
        self.path = req_line[1]
        self.http_version = req_line[2]

        headers = {}

        for line in lines:
            if line:
                lst = line.split(':')
                headers[lst[0]] = lst[1].strip()

        self.headers = headers

    def get_path(self):
        return self.path