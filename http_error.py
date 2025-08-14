class HTTPError(Exception):
    def __init__(self, title=b'Internal Server Error', status=b'500', message=b'The server encountered an unexpected condition which prevented it from fulfilling the request.'):
        self.title = title
        self.status = status
        self.message = message

    def response_html(self):
        return b'<!doctype html><html><head><title>%b %b</title></head><body><h1>%b</h1><p>%b</p></body></html>' % (self.status, self.title, self.title, self.message)


class HTTPBadRequestError(HTTPError):
    def __init__(self, status=b'400', title=b'Bad Request', message=b'The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications.'):
        super().__init__(title, status, message)