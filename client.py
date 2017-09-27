from socket import socket

class Client():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket()

    def connect():
        self.socket.connect(self.ip, self.port)

    def send_request(request):
        self.socket.send(request)

