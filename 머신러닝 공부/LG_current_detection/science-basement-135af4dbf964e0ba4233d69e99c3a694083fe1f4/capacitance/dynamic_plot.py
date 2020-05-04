import numpy as np
import matplotlib.pyplot as plt

class DynamicPlot():
    def __init__(self, x_data, major_grid, minor_grid):
        # create plot
        plt.ion()
        self.ax = plt.gca() 
        self.line, = self.ax.plot(x_data, np.zeros(len(x_data)))
        self.autoscale = True
        
        # Enable major or minor grid lines
        if (major_grid):
            if (minor_grid):
                self.ax.minorticks_on()
            self.ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')
            self.ax.grid(which='minor', linestyle=':', linewidth='0.5', color='grey')
    
    def format_x(self, label, min, max):
        self.ax.set_xlim([min, max])
        plt.xlabel(label)

    def format_y(self, label, min=0, max=0):
        self.autoscale = True
        if (min != max):
            self.ax.set_ylim([min, max])
            self.autoscale = False
        plt.ylabel(label)     
        
    def update_x(self, data):
        self.line.set_xdata(data)
        if (self.autoscale):
            self.ax.relim()
            self.ax.autoscale_view()
        plt.draw()
        plt.pause(0.001)
        
    def update_y(self, data):
        self.line.set_ydata(data)
        if (self.autoscale):
            self.ax.relim()
            self.ax.autoscale_view()
        plt.draw()
        plt.pause(0.001)

    def opened(self):
        return plt.get_fignums()


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
