class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        splits = request.split(b'\r\n\r\n',1)
        Headers = splits[0].decode().split('\r\n')
        [self.method, self.path, self.http_version] = Headers[0].split(' ')
        self.cookies = {}
        self.headers = {}
        Headers = Headers[1:]
        for header in Headers:
            headers_splits = header.split(':',1)
            self.headers[headers_splits[0]] = headers_splits[1].strip()
        if len(splits) > 1:
            self.body = splits[1]
        else:
            self.body = b""
        if "Cookie" in self.headers:
            cookies = self.headers["Cookie"].split(";")
            for i in cookies:
                head = i[:i.find('=')].strip()
                tail = i[i.find('=')+1:].strip()
                self.cookies[head] = tail





def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct
def test2():
    request = Request(b'GET /sample_page.html HTTP/2.0\r\nHost: www.google.com\r\nCookie: cookie1=chocolate; cookie2=strawberry\r\n\r\nHello World!')


if __name__ == '__main__':
    test1()
    test2()
