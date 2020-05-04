import numpy as np
import matplotlib.pyplot as plt

class DynamicPlot():
    def __init__(self, x_data, major_grid, minor_grid):
        # create plot
        plt.ion()
        self.ax = plt.gca() 
        self.line, = self.ax.plot(x_data, np.zeros(len(x_data)))
        
        # Enable major or minor grid lines
        if (major_grid):
            if (minor_grid):
                self.ax.minorticks_on()
            self.ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')
            self.ax.grid(which='minor', linestyle=':', linewidth='0.5', color='grey')
    
    def format_x(self, min, max, label):
        self.ax.set_xlim([min, max])
        plt.xlabel(label)
    
    def format_y(self, min, max, label):
        self.ax.set_ylim([min, max])
        plt.ylabel(label)    
        
    def update_x(self, data):
        self.line.set_xdata(data)
        plt.draw()
        plt.pause(0.001)
        
    def update_y(self, data):
        self.line.set_ydata(data)
        plt.draw()
        plt.pause(0.001)

    def opened(self):
        return plt.get_fignums()
        