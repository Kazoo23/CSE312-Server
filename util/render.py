from util.response import Response
import os

def renderindex(request,handler):
    res = Response()
    templatefile = open(os.path.join('public','layout','layout.html'), 'r').read()
    indexfile = open(os.path.join('public','index.html'),'r').read()
    indexfile = templatefile.replace("{{content}}",indexfile)
    res.headers({'Content-Type' : 'text/html; charset=utf-8'})
    indexfile = indexfile.encode()
    res.bytes(indexfile)
    handler.request.sendall(res.to_data())

def renderchat(request,handler):
    res = Response()
    templatefile = open(os.path.join('public','layout','layout.html'), 'rb').read()
    chatfile = open(os.path.join('public','chat.html'),'rb').read()
    chatfile = templatefile.replace(b"{{content}}",chatfile)
    res.bytes(chatfile)
    res.headers({'Content-Type' : 'text/html; charset=utf-8'})
    handler.request.sendall(res.to_data())

def renderFile(request,handler):
    res = Response()
    path = request.path.lstrip('/')
    path = path.split('/')
    file = open(os.path.join(*path),'rb').read()
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