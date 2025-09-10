import json


class Response:
    def __init__(self):
        self.stat = '200 OK'
        self.head = {"X-Content-Type-Options": 'nosniff'}
        self.cook = {}
        self.bdy = b""
        pass

    def set_status(self, code, text):
        self.stat = str(code) + ' ' + text
        return self

    def headers(self, headers):
        self.head.update(headers)
        return self

    def cookies(self, cookies):
        for x in cookies:
            self.cook.update({str(x): str(cookies[x])})
        return self

    def bytes(self, data):
        self.bdy += data
        return self

    def text(self, data):
        self.bdy += data.encode()
        return self

    def json(self, data):
        self.headers({'Content-Type' : 'application/json'})
        self.bdy = json.dumps(data).encode()
        return self

    def to_data(self):
        res = b'HTTP/1.1 ' + self.stat.encode()
        if 'Content-Type' not in self.head:
            self.headers({'Content-Type' : 'text/plain; charset=utf-8'})
        for i in self.head:
            res += b'\r\n' + i.encode() + b': ' + self.head[i].encode()
        for cook in self.cook:
            res += b'\r\nSet-Cookie: ' + cook.encode() + b'=' + self.cook[cook].encode()
        res += b'\r\nContent-Length: ' + str(len(self.bdy)).encode()
        res += b'\r\n\r\n' + self.bdy
        return res


def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()
    #assert expected == actual
def test2():
    res = Response()
    res.cookies({"cookie1":"value1","cookie2":"value2"})
    print(res.to_data())

if __name__ == '__main__':
    test1()
    test2()