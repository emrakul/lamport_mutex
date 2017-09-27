import heapq

from rpc import RPC
import fcntl
import time



class LamportMutex:


    def __init__(self, pid, port, other_pids, other_ports, file_location='mutex.txt'):
        self._queue = list()
        self.pid = pid
        self.port = port
        self.file_location = 'mutex.txt'
        self.rpc = RPC(pid, port, other_pids, other_ports, self.request_cb, self.release_cb)

    def request_cb(self, pid, clock, event_id):
        heapq.heappush(self._queue, (int(clock), pid))
        self.rpc.reply(pid, event_id)

    def release_cb(self, pid, clock, event_id):
        self._queue = list(filter(lambda x: x[1]!=self.pid, self._queue))
        heapq.heapify(self._queue)
        self.rpc.reply(pid, event_id)
    

    def lock_unlock(self):
        heapq.heappush(self._queue, (self.rpc.clock.get_clock(), self.pid))
        self.rpc.request()
        while self._queue[0][1] != self.pid:
            time.sleep(0.1)

        lamport_clock = self.rpc.clock.increment()
        with open(self.file_location, 'a') as file:
            try:
                fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                print("ERROR:", self.pid, lamport_clock)
            file.write("{} {} acquire\n".format(self.pid, lamport_clock))
            self._queue.pop()
            lamport_clock = self.rpc.clock.increment()
            fcntl.flock(file, fcntl.LOCK_UN)
            file.write("{} {} release\n".format(self.pid, lamport_clock))
        self.rpc.release()

