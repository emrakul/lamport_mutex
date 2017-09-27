'''
class Message():
    def __init__(self, from_, to, clock, content):
        self.from_ = from_
        self.to = to
        self.clock = clock
        self.content = content
    def __le__(self, other):
        if self.clock > other.clock:
            return +1;
        elif self.clock < other.clock:
            return -1;
        else:
            
'''
