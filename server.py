from socket import socket, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
import sys

MAX_SIZE = 100

class Server():

    def __init__(self, pid, port):
        self.pid = pid
        self.port = port
        self._socket = socket()
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._socket.bind(('localhost', int(self.port)))
        self._socket.listen(MAX_SIZE)
        self.clients = []


    def close(self):
        self._socket.close()

    def accept(self, num_others):
        for _ in range(num_others):
            conn, _ = self._socket.accept()
            self.clients.append(conn)
        return [conn.fileno() for conn in self.clients]
