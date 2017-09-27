import select
class Poll:
    def __init__(self):
        self._kqueue = select.kqueue()

    def control(self, fd):
        kev = select.kevent(fd, select.KQ_FILTER_READ, select.KQ_EV_ADD | select.KQ_EV_ENABLE)
        self._kqueue.control([kev], 0, 0)

    def poll(self):
        while True:
            fd = self._kqueue.control([], 1, None)[0].ident
            return fd
