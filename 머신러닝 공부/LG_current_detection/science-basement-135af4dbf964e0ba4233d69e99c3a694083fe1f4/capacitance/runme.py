#!/usr/bin/python

import time
import sys
import numpy as np

#import pi_spi
import fdc2214 as fdc

enable_plot = True
time_step = 0.1     # sec, plotting takes ~0.4
buffer_size = 200   # nr of samples

if (enable_plot):
    import dynamic_plot as dp

fdc2214 = fdc.FDC2214(115200, 'COM5')

print ("Press CTRL-C to exit")
try:
    time_min = 0
    time_max = buffer_size * time_step
    C_min = -3; C_max = 3;

    if (enable_plot):
        buffer = dp.RingBuffer(buffer_size)
        plot = dp.DynamicPlot(np.linspace(time_min, time_max, buffer_size), True, True)
        plot.format_x('Time / sec', time_min, time_max)
        plot.format_y('C / pF') #, C_min, C_max)

    #dout = pi_spi.PiSpi_8KO(True)
    #dout.write(0)
    active_cntr = 0

    keep_looping = True
    while(keep_looping):
        t1 = time.time()

        # read parameters from file
        filehandle = open('c:/Users/pilwook/Documents/GitHub/AIseminar/머신러닝 공부/LG_current_detection/science-basement-135af4dbf964e0ba4233d69e99c3a694083fe1f4/capacitance/please.txt', mode='r')
        data = filehandle.readlines()
        #data=0.22
        filehandle.close()

        if (len(data) < 2):
            print("Invalid data in file", data_file_name)
            sys.exit(0)
        
        # parse zeroing & threshold capacitance and # counts needed to activate output
        [C0, C1, cntr_max] = [float(data[0].strip()), float(data[1].strip()), int(data[2].strip())]

        # based on capacitance value, decide either to activate or close output
        C = round(fdc2214.read_ch1(), 3) - C0
        if (abs(C) < C1 and active_cntr != 0):
            active_cntr = 0
            #dout.write(0)
        else:
            active_cntr += 1
            if (active_cntr > cntr_max):
                active_cntr = 0
                #dout.write(255)

        print("\rC = %.3f pF" % C, end='')
        
        # add measurement to the graph
        if(enable_plot):
            buffer.append(C)
            plot.update_y(buffer.get_lifo())
            keep_looping = plot.opened()

        time.sleep(max(0, time_step - (time.time() - t1)))

            
except KeyboardInterrupt:   # Press CTRL C to exit Program
    fdc.close()
    sys.exit(0)
