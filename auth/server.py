import socketserver
import time


from util.request import Request
from util.router import Router
from util.hello_path import hello_path
from util.render import renderFile
from util.chat import createChat
from util.chat import getChats
from util.chat import updateChat
from util.chat import deleteChat
from util.account import register
from util.account import login
from util.account import logout
from util.account import user
from util.account import update
from util.account import search
from util.account import generatetwofa
from util.account import githubauth
from util.account import githubauthcode
from util.imagehandle import profileimgupdate
from util.videos import upload
from util.videos import getallvideos
from util.videos import getsinglevideo
from util.videos import updatethumbnail
from util.websockets import websocketConnect
from util.websockets import createCall

class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.router = Router()
        self.router.add_route("GET", "/hello", hello_path, True)
        self.router.add_route("GET","/",renderFile, True)
        self.router.add_route("GET","/chat",renderFile, False)
        self.router.add_route("GET","/public",renderFile, False)
        self.router.add_route("POST", "/api/chats", createChat, False)
        self.router.add_route("GET", "/api/chats", getChats, False)
        self.router.add_route("PATCH", "/api/chats", updateChat, False)
        self.router.add_route("DELETE", "/api/chats", deleteChat, False)
        self.router.add_route("GET", "/register", renderFile, True)
        self.router.add_route("GET", "/login", renderFile, True)
        self.router.add_route("GET", "/settings", renderFile, True)
        self.router.add_route("GET", "/search-users", renderFile, True)
        self.router.add_route("POST", "/register", register, True)
        self.router.add_route("POST", "/login", login, True)
        self.router.add_route("GET", "/logout", logout, True)
        self.router.add_route("GET", "/api/users/@me", user, True)
        self.router.add_route("POST", "/api/users/settings", update, True)
        self.router.add_route("GET", "/api/users/search", search, False)
        self.router.add_route("POST", "/api/totp/enable", generatetwofa, False)
        self.router.add_route("GET", "/authgithub", githubauthcode, False)
        self.router.add_route("GET", "/authcallback", githubauth, False)
        self.router.add_route("GET", "/change-avatar", renderFile, True)
        self.router.add_route("POST", "/api/users/avatar", profileimgupdate, False)
        self.router.add_route("GET", "/videotube", renderFile, True)
        self.router.add_route("GET", "/videotube/upload", renderFile, True)
        self.router.add_route("GET", "/videotube/videos", renderFile, False)
        self.router.add_route("POST", "/api/videos", upload, True)
        self.router.add_route("GET", "/api/videos", getallvideos, True)
        self.router.add_route("GET", "/api/videos/", getsinglevideo, False)
        self.router.add_route("GET", "/videotube/set-thumbnail", renderFile, False)
        self.router.add_route("PUT", "/api/thumbnails/", updatethumbnail, False)
        self.router.add_route("GET", "/test-websocket", renderFile, True)
        self.router.add_route("GET", "/drawing-board", renderFile, True)
        self.router.add_route("GET", "/video-call", renderFile, True)
        self.router.add_route("GET", "/video-call/", renderFile, False)
        self.router.add_route("GET", "/websocket", websocketConnect, True)
        self.router.add_route("POST", "/api/video-calls", createCall, True)
        # TODO: Add your routes here
        super().__init__(request, client_address, server)

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)
        if request.headers.get("Content-Length") is not None and int(request.headers.get("Content-Length")) > len(request.body):
            starttime = time.time()
            while request.headers.get("Content-Length") is not None and int(request.headers.get("Content-Length")) > len(request.body):
                if (time.time() - starttime) > 0.5:
                    return
                content = self.request.recv(2048)
                if content is None:
                    return
                request.body += content
        self.router.route_request(request, self)


def main():
    host = "0.0.0.0"
    port = 8080
    socketserver.ThreadingTCPServer.allow_reuse_address = True

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
