from util.response import Response
import os

def renderindex(request,handler):
    res = Response()
    templatefile = open('public\\layout\\layout.html','rb').read()
    indexfile = open('public\index.html','rb').read()
    indexfile = templatefile.replace(b"{{content}}",indexfile)
    res.headers({'Content-Type' : 'text/html; charset=utf-8'})
    res.bytes(indexfile)
    handler.request.sendall(res.to_data())

def renderchat(request,handler):
    res = Response()
    templatefile = open('public\\layout\\layout.html','rb').read()
    chatfile = open('public\chat.html','rb').read()
    chatfile = templatefile.replace(b"{{content}}",chatfile)
    res.headers({'Content-Type' : 'text/html; charset=utf-8'})
    res.bytes(chatfile)
    handler.request.sendall(res.to_data())

def renderFile(request,handler):
    res = Response()
    file = open(request.path[1:],'rb').read()
    res.bytes(file)
    if '.jpg' in request.path:
        head = {'Content-Type': 'image/jpeg'}
    elif '.png' in request.path:
        head = {'Content-Type': 'image/png'}
    elif '.ico' in request.path:
        head = {'Content-Type': 'image/x-icon'}
    elif '.gif' in request.path:
        head = {'Content-Type': 'image/gif'}
    elif '.webp' in request.path:
        head = {'Content-Type': 'image/webp'}
    elif '.html' in request.path:
        head = {'Content-Type': 'text/html; charset=utf-8'}
    elif '.js' in request.path:
        head = {'Content-Type': 'application/javascript'}
    elif '.css' in request.path:
        head = {'Content-Type': 'text/css'}
    else:
        res.set_status("404","Not Found")
        res.text("Non-known data type")
        handler.request.sendall(res.to_data())
        return
    res.headers(head)
    handler.request.sendall(res.to_data())