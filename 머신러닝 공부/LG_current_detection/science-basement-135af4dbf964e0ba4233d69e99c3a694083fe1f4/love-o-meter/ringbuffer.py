import numpy as np

class RingBuffer():
    "A 1D ring buffer using numpy arrays"
    def __init__(self, length):
        self.data = np.empty(length, dtype='f')
        self.data[:] = np.NAN
        self.index = 0

    def append(self, x):
        "adds float x to ring buffer"
        self.data[self.index] = x
        self.index = (self.index + 1) % self.data.size
        
    def extend(self, x):
        "adds array x to ring buffer"
        x_index = (self.index + np.arange(x.size)) % self.data.size
        self.data[x_index] = x
        self.index = x_index[-1] + 1

    def get_fifo(self):
        "Returns the first-in-first-out data in the ring buffer"
        idx = (self.index + np.arange(self.data.size)) %self.data.size
        return self.data[idx]
        
    def get_lifo(self):
        "Returns the first-in-last-out data in the ring buffer"
        idx = (np.arange(self.data.size - 1, -1, -1) + self.index) %self.data.size
        return self.data[idx]

def ringbuff_numpy_test():
    ringlen = 4
    ringbuff = RingBuffer(ringlen)
    for i in range(1,6):
        #ringbuff.extend(np.zeros(10000, dtype='f')) # write
        ringbuff.append(1.0 * i) # write
        print(ringbuff.get_fifo()) #read
        print(ringbuff.get_lifo()) #read
        print(" ")