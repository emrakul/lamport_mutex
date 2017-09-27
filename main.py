from lamport import LamportMutex
from parse import parse
from multiprocessing import Process
import sys
import time

def proc(i, j):
    pids, ports = parse('config.cfg')
    current_pid = pids[i]
    current_port = ports[i]
    pids.remove(current_pid)
    ports.remove(current_port)
    lamport = LamportMutex(current_pid, current_port, pids, ports)
    time.sleep(5) #Initializtion time to avoid self-deadlock (callback referencing itself)
    while True:
        lamport.lock_unlock()


if __name__ == "__main__":
    procs = []
    for i in range(10):
        procs.append(Process(target=proc, args=(i, None)))
    for proc_ in procs:
        proc_.start()
    for proc_ in procs:
        proc_.join()
