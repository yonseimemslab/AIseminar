import time
import numpy as np

import drdaq
import tools
import ringbuffer as rb
import dynamicplot as dp
import serialreader as sr

buffer_size = 240   # samples
time_step = 0.5     # sec, plotting takes ~0.4

time_min = 0; time_max = buffer_size * time_step;
temp_min = 18; temp_max = 28;
#temp_min = 0; temp_max = 1;

drdaq.init()
buffer = rb.RingBuffer(buffer_size)
serial = sr.SerialReader(9600, '/dev/ttyACM0')
plot = dp.DynamicPlot(np.linspace(time_min, time_max, buffer_size), True, True)
plot.format_x(time_min, time_max, 'Time [sec]')
plot.format_y(temp_min, temp_max, 'Temperature [$^\circ$C]')
  
t0 = time.time()
while(plot.opened()):
    t1 = time.time()
    #temperature = tools.get_random()
    temperature = max(drdaq.get_ext1(), drdaq.get_temperature())  # [degC]
    #temperature = serial.read_line()
    #serial.write_line("%.1f" % temperature)
    
    buffer.append(temperature)
    plot.update_y(buffer.get_lifo())
    
    print("\rElapsed time: %.1f sec, T = %.1f C" % (time.time() - t0, temperature), end='')
    #time.sleep(max(0, time_step - (time.time() - t1)))

serial.close()
print("\n")
