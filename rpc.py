import time
import os
import time
from socket import socket
from client import Client
from server import Server
from clock import Clock
from channel import Channel
import event

from serialize import deserialize

class RPC:
    def __init__(self, pid, port, other_pids, other_ports, request_cb, release_cb):
        self.pid = pid
        self.port = port
        self.other_pids = other_pids
        self.other_ports = other_ports
        self.clock = Clock()
        self.request_cb = request_cb
        self.release_cb = release_cb
        self.channel = Channel(pid, port, other_pids, other_ports, self.on_event)
        self.replies = 0

        
    def broadcast(self, msg):
        self.channel.broadcast()

    def on_event(self, msg):
        pid, clock, event_id = deserialize(msg)
        if event_id == event.REQUEST:
            self.clock.clock = max(self.clock.get_clock()+1, int(clock))
            self.request_cb(pid, clock, event_id)

        if event_id == event.RELEASE:
            self.clock.clock = max(self.clock.get_clock()+1, int(clock))
            self.release_cb(pid, clock, event_id)

        if event_id == event.REPLY:
            self.replies += 1
            self.last_event = self.clock.get_clock()

    def request(self):
        self.replies = 0
        for other_pid in self.other_pids:
            self.clock.increment()
            self.channel.send(other_pid, self.clock.get_clock(), event.REQUEST)
        while self.replies < len(self.other_pids):
            time.sleep(0.1)

    def release(self):
        for other_pid in self.other_pids:
            self.clock.increment()
            self.channel.send(other_pid, self.clock.get_clock(), event.RELEASE)

    def reply(self, to_id, event_id):
        self.clock.increment()
        self.channel.send(to_id, self.clock, event.REPLY)





