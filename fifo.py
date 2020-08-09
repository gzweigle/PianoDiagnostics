# Gregary C. Zweigle
# 2020
import collections
import numpy as np

class Fifo:

    def __init__(self, fifo_length):
        self.fifo = collections.deque(maxlen=fifo_length)
        self.fifo_length = fifo_length
        self.print_count = 0

    def put(self, data):
        if len(self.fifo) < self.fifo_length:
            self.fifo.append(data)
        else:
            # This should never happen so, want to see when it does.
            print('FIFO No Put {0}'.format(self.print_count))
            self.print_count += 1
            if self.print_count > 9:
                self.print_count = 0

    def hard_put(self, data):
        self.fifo.append(data)

    def get(self):
        try:
            data = self.fifo.popleft()
            data_valid = True
        except IndexError:
            data = 0
            data_valid = False
        return data, data_valid
