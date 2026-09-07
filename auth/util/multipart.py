from util.request import Request
from util.multipartclass import MultipartRequest
from util.multipartclass import MultipartPart

def parse_multipart(request):
    mult = MultipartRequest()
    mult.boundary = request.headers["Content-Type"].split(";")[1].split("=")[1]
    parts = request.body.split(b"--" + mult.boundary.encode(),1)[1]
    parts = parts.split(b"\r\n--" + mult.boundary.encode() + b'--')[0]
    parts= parts.split(b"\r\n--" + mult.boundary.encode())
    for part in parts:
        temppart = MultipartPart()
        #print(part)
        headers,temppart.content = part.split(b"\r\n\r\n", 1)
        temppart.content = temppart.content.rstrip(b"\r\n")
        headers = headers.decode().split("\r\n")
        if headers[0] == "":
            headers = headers[1:]
        for header in headers:
            #print(header)
            value,body = header.split(":")
            temppart.headers[value] = body.strip()
        temppart.name = temppart.headers["Content-Disposition"].split('name="',1)[1].split('"')[0]
        mult.parts.append(temppart)
    return mult

def test1():
    request = Request(b"POST /form-path HTTP/1.1\r\nContent-Length: 9937\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarycriD3u6M0UuPR1ia\r\n\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name=\"commenter\"\r\n\r\nJesse\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"discord.png\"\r\nContent-Type: image/png\r\n\r\n<bytes_of_the_file>\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia--\r\n")
    mult = parse_multipart(request)
    print("---Test1---")
    print(mult.boundary)
    for part in mult.parts:
        print(part.name)
        print(part.headers)
        print(part.content)
def test2():
    request = Request(b"POST /form-path HTTP/1.1\r\nHost: localhost:8080\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarySinglePart\r\nContent-Length: 123\r\n\r\n------WebKitFormBoundarySinglePart\r\nContent-Disposition: form-data; name=\"commenter\"\r\n\r\nJesse\r\n------WebKitFormBoundarySinglePart--\r\n")
    mult = parse_multipart(request)
    print("---Test2---")
    print(mult.boundary)
    for part in mult.parts:
        print(part.name)
        print(part.headers)
        print(part.content)

if __name__ == '__main__':
    test1()
    test2()