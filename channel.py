from socket import socket
from threading import Thread
from client import Client
from server import Server
from poll import Poll
from serialize import serialize
import time
import errno
import os

class Channel:
    def __init__(self, pid, port, other_pids, other_ports, on_event, logger=None):
        self.pid = pid
        self.port = port
        self.other_pids = other_pids
        self.other_ports = other_ports

        self.server = Server(pid, port)
        self.poll = Poll()
        
        self.connections = {}
        for i, pid in enumerate(other_pids):
            while True:
                try:
                    self.connections[pid] = socket()
                    self.connections[pid].connect(('localhost', int(other_ports[i])))
                    break
                except (ConnectionRefusedError, OSError):
                    continue

        print(self.pid, self.connections)

        #self.client = Client(pid, port)
        conns = self.server.accept(len(self.other_ports))
        print(conns)
        for fd in conns:
            self.poll.control(fd)
        print('poll create')

        self.on_event = on_event
        self.thr = Thread(target=self.events_loop)
        self.thr.start()


    def send(self, to_pid, clock, event):
        self.connections[to_pid].send(serialize(self.pid, clock, event))

    def pass_to_server(self, message):
        self.server.process(deserialize(message))

    def broadcast(self, message):
        for connection in connections:
            connection.send(message)

    def read_event(self, fd):
        c = os.read(fd, 1)
        msg = ""
        while (c.decode() != '\n'):
            msg += c.decode()
            c = os.read(fd, 1)
        return msg

    def events_loop(self):
        while True:
            fd = self.poll.poll()
            event = self.read_event(fd)
            self.on_event(event)
            #yield event
