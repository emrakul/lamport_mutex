class Clock:
    def __init__(self):
        self.clock = 0

    def increment(self):
        self.clock += 1
        return self.get_clock()

    def update(self, other):
        self.clock += 1
        self.clock = max(self.clock, other.clock)

    def get_clock(self):
        return self.clock
