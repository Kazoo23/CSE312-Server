from util.response import Response
from util.request import Request
import os

def renderFile(request,handler):
    res = Response()
    if(request.path=='/'):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        indexfile = open(os.path.join('public', 'index.html'), 'rb').read()
        indexfile = templatefile.replace(b"{{content}}", indexfile)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        res.bytes(indexfile)
        handler.request.sendall(res.to_data())
        return
    if(request.path=='/chat'):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        chatfile = open(os.path.join('public', 'chat.html'), 'rb').read()
        chatfile = templatefile.replace(b"{{content}}", chatfile)
        res.bytes(chatfile)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if(request.path=='/register'):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        registerfile = open(os.path.join('public', 'register.html'), 'rb').read()
        registerfile = templatefile.replace(b"{{content}}", registerfile)
        res.bytes(registerfile)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if (request.path == '/login'):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        loginfile = open(os.path.join('public', 'login.html'), 'rb').read()
        loginfile = templatefile.replace(b"{{content}}", loginfile)
        res.bytes(loginfile)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if (request.path == '/settings'):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        settingsfile = open(os.path.join('public', 'settings.html'), 'rb').read()
        settingsfile = templatefile.replace(b"{{content}}", settingsfile)
        res.bytes(settingsfile)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if (request.path == '/search-users'):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        searchfile = open(os.path.join('public', 'search-users.html'), 'rb').read()
        searchfile = templatefile.replace(b"{{content}}", searchfile)
        res.bytes(searchfile)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if (request.path == '/change-avatar'):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        avatar = open(os.path.join('public', 'change-avatar.html'), 'rb').read()
        avatar = templatefile.replace(b"{{content}}", avatar)
        res.bytes(avatar)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if (request.path == '/videotube'):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        video = open(os.path.join('public', 'videotube.html'), 'rb').read()
        video = templatefile.replace(b"{{content}}", video)
        res.bytes(video)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if (request.path == '/videotube/upload'):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        video = open(os.path.join('public', 'upload.html'), 'rb').read()
        video = templatefile.replace(b"{{content}}", video)
        res.bytes(video)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if ('videotube/videos' in request.path):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        video = open(os.path.join('public', 'view-video.html'), 'rb').read()
        video = templatefile.replace(b"{{content}}", video)
        res.bytes(video)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if ('videotube/set-thumbnail' in request.path):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        video = open(os.path.join('public', 'set-thumbnail.html'), 'rb').read()
        video = templatefile.replace(b"{{content}}", video)
        res.bytes(video)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if ('test-websocket' in request.path):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        video = open(os.path.join('public', 'test-websocket.html'), 'rb').read()
        video = templatefile.replace(b"{{content}}", video)
        res.bytes(video)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if ('drawing-board' in request.path):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        video = open(os.path.join('public', 'drawing-board.html'), 'rb').read()
        video = templatefile.replace(b"{{content}}", video)
        res.bytes(video)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if (request.path == '/video-call'):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        video = open(os.path.join('public', 'video-call.html'), 'rb').read()
        video = templatefile.replace(b"{{content}}", video)
        res.bytes(video)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
    if ('/video-call/' in request.path):
        templatefile = open(os.path.join('public', 'layout', 'layout.html'), 'rb').read()
        video = open(os.path.join('public', 'video-call-room.html'), 'rb').read()
        video = templatefile.replace(b"{{content}}", video)
        res.bytes(video)
        res.headers({'Content-Type': 'text/html; charset=utf-8'})
        handler.request.sendall(res.to_data())
        return
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
        head = {'Content-Type': 'text/javascript; charset=utf-8'}
    elif '.css' in request.path:
        head = {'Content-Type': 'text/css; charset=utf-8'}
    elif '.txt' in request.path:
        head = {'Content-Type': 'text/plain; charset=utf-8'}
    elif '.mp4' in request.path:
        head = {'Content-Type': 'video/mp4'}
    elif '.m3u8' in request.path:
        head = {'Content-Type': 'application/vnd.apple.mpegurl'}
    elif '.ts' in request.path:
        head = {'Content-Type': 'video/mp2t'}
    else:
        res.set_status("404","Not Found")
        res.text("Non-known data type")
        handler.request.sendall(res.to_data())
        return
    res.headers(head)
    handler.request.sendall(res.to_data())
