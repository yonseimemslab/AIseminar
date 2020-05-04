#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import collections
import serial
import time
import struct
#import msvcrt
from array import *
import binascii
import numpy as np
import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
#threading
import threading

#############################################################################################
# LDC1000 addressing space
LDC1614_DATA_MSB_CH0        = '00'
LDC1614_DATA_LSB_CH0        = '01'
LDC1614_DATA_MSB_CH1        = '02'
LDC1614_DATA_LSB_CH1        = '03'
LDC1614_DATA_MSB_CH2        = '04'
LDC1614_DATA_LSB_CH2        = '05'
LDC1614_DATA_MSB_CH3        = '06'
LDC1614_DATA_LSB_CH3        = '07'
LDC1614_RCOUNT_CH0          = '08'
LDC1614_RCOUNT_CH1          = '09'
LDC1614_RCOUNT_CH2          = '0A'
LDC1614_RCOUNT_CH3          = '0B'
LDC1614_OFFSET_CH0          = '0C'
LDC1614_OFFSET_CH1          = '0D'
LDC1614_OFFSET_CH2          = '0E'
LDC1614_OFFSET_CH3          = '0F'
LDC1614_SETTLECOUNT_CH0     = '10'
LDC1614_SETTLECOUNT_CH1     = '11'
LDC1614_SETTLECOUNT_CH2     = '12'
LDC1614_SETTLECOUNT_CH3     = '13'
LDC1614_CLOCK_DIVIDERS_CH0  = '14'
LDC1614_CLOCK_DIVIDERS_CH1  = '15'
LDC1614_CLOCK_DIVIDERS_CH2  = '16'
LDC1614_CLOCK_DIVIDERS_CH3  = '17'
LDC1614_STATUS              = '18'
LDC1614_ERROR_CONFIG        = '19'
LDC1614_CONFIG              = '1A'
LDC1614_MUX_CONFIG          = '1B'
LDC1614_RESET_DEV           = '1C'
LDC1614_DRIVE_CURRENT_CH0   = '1E'
LDC1614_DRIVE_CURRENT_CH1   = '1F'
LDC1614_DRIVE_CURRENT_CH2   = '20'
LDC1614_DRIVE_CURRENT_CH3   = '21'
LDC1614_MANUFACTURER_ID     = '7E'
LDC1614_DEVICE_ID           = '7F'


DEBUG_PRINT_TX_DATA = 0
DEBUG_PRINT_RX_DATA = 0
DEBUG_PRINT_READ_DATA = 0

class crc8:
    def __init__(self):
        self.crcTable = (0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 0x38,
                         0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d, 0x70, 0x77,
                         0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 0x48, 0x4f, 0x46,
                         0x41, 0x54, 0x53, 0x5a, 0x5d, 0xe0, 0xe7, 0xee, 0xe9,
                         0xfc, 0xfb, 0xf2, 0xf5, 0xd8, 0xdf, 0xd6, 0xd1, 0xc4,
                         0xc3, 0xca, 0xcd, 0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b,
                         0x82, 0x85, 0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba,
                         0xbd, 0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2,
                         0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea, 0xb7,
                         0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2, 0x8f, 0x88,
                         0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a, 0x27, 0x20, 0x29,
                         0x2e, 0x3b, 0x3c, 0x35, 0x32, 0x1f, 0x18, 0x11, 0x16,
                         0x03, 0x04, 0x0d, 0x0a, 0x57, 0x50, 0x59, 0x5e, 0x4b,
                         0x4c, 0x45, 0x42, 0x6f, 0x68, 0x61, 0x66, 0x73, 0x74,
                         0x7d, 0x7a, 0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b,
                         0x9c, 0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,
                         0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 0xc1,
                         0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4, 0x69, 0x6e,
                         0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c, 0x51, 0x56, 0x5f,
                         0x58, 0x4d, 0x4a, 0x43, 0x44, 0x19, 0x1e, 0x17, 0x10,
                         0x05, 0x02, 0x0b, 0x0c, 0x21, 0x26, 0x2f, 0x28, 0x3d,
                         0x3a, 0x33, 0x34, 0x4e, 0x49, 0x40, 0x47, 0x52, 0x55,
                         0x5c, 0x5b, 0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64,
                         0x63, 0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b,
                         0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13, 0xae,
                         0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 0x96, 0x91,
                         0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83, 0xde, 0xd9, 0xd0,
                         0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 0xe6, 0xe1, 0xe8, 0xef,
                         0xfa, 0xfd, 0xf4, 0xf3)
    def crc(self, msg):
        runningCRC = 0
        for c in msg:
            c = ord(str(c))
            runningCRC = self.crcByte(runningCRC, c)
        return runningCRC
    
    def crcByte(self, oldCrc, byte):
        res = self.crcTable[oldCrc & 0xFF ^ byte & 0xFF];
        return res

def write_reg(serial_port, addr, data):
    crc = crc8()
    serial_string = '4C150100042A'+ addr + data
    serial_string = serial_string.decode('hex')
    crc_byte = chr(crc.crc(serial_string))
    serial_port.write(serial_string+crc_byte)
    s = serial_port.read(32)
    if DEBUG_PRINT_RX_DATA:
        print("Read:%s" % (binascii.hexlify(s)))
    if (s[3] != '\x00'):
        print("Error in write register")
        exit()

def read_reg(serial_port, addr):
    
    crc = crc8()
    serial_string = '4C150100022A'+ addr
    serial_string = serial_string.decode('hex')
    crc_byte = chr(crc.crc(serial_string))
    serial_port.write(serial_string+crc_byte)
    s = serial_port.read(32)
    if DEBUG_PRINT_RX_DATA:
        print("Read:%s" % (binascii.hexlify(s)))
    if (s[3] != '\x00'):
        print("Error in set register")
        exit()
    serial_string = '4C140100022A02'
    serial_string = serial_string.decode('hex')
    crc_byte = chr(crc.crc(serial_string))
    serial_port.write(serial_string+crc_byte)
    s = serial_port.read(32)
    if DEBUG_PRINT_RX_DATA:
        print("Read:%s" % (binascii.hexlify(s)))
    if (s[3] != '\x00'):
        print("Error in read register")
        exit()
    data_read = s[6] + s[7]
    if DEBUG_PRINT_READ_DATA:
        print("Addr:", addr,"Data:", binascii.hexlify(data_read) )
    return binascii.hexlify(data_read)

def ldc_config(serial_port):
    write_reg(serial_port, LDC1614_CONFIG,'C20C') #channel, C20C -> 4 channels -> 1 10(4 chs) 0001000001 100 (3.3mhz) 
                                                            #820C -> 4 channels -> 1 00(ch 0) 0001000001 100 (3.3mhz)


def ldc_start_streaming(serial_port):
    #start streaming
    serial_stream_string = '4C0501000601290404302AC1'
    serial_stream_string = serial_stream_string.decode('hex')
    crc = crc8()
    crc_byte = chr(crc.crc(serial_stream_string))
    serial_port.write(serial_stream_string+crc_byte)
    s = serial_port.read(32)
    if DEBUG_PRINT_RX_DATA:
        print("Read:%s" % (binascii.hexlify(s)))
    if (s[3] != '\x00'):
        print("Error in write register")
        exit()

def ldc_stop_streaming(serial_port):
    #stop streaming
    serial_stop_stream_string = '4C0601000101D2'
    serial_stop_stream_string = serial_stop_stream_string.decode('hex')
    crc = crc8()
    crc_byte = chr(crc.crc(serial_stop_stream_string))
    serial_port.write(serial_stop_stream_string+crc_byte)
    s = serial_port.read(32)
    if DEBUG_PRINT_RX_DATA:
        print("Read:%s" % (binascii.hexlify(s)))
    if (s[3] != '\x00'):
        print("Error in write register")
        exit()

#initilize the channle buffers
ch0_buf = deque(0 for _ in range(5000))
ch1_buf = deque(0 for _ in range(5000))
ch2_buf = deque(0 for _ in range(5000))
ch3_buf = deque(0 for _ in range(5000))
avg = 0

def AddValue(val):
    global avg

    ch0_buf.append(val)
    ch0_buf.popleft()

    avg = avg + 0.1*(val-avg)
    ch1_buf.append(avg)
    ch1_buf.popleft()

def AddValues(val, ch):
    ch.append(val)
    ch.popleft()

def msp430():
    t = threading.currentThread()

    serial_port = serial.Serial(port='COM3', baudrate=115200)
    device_id   = read_reg  (serial_port, LDC1614_DEVICE_ID)
    print("device_id=%s" % (device_id))

    #modify the registration, sample
    ldc_config (serial_port)
    write_reg (serial_port, LDC1614_CONFIG, '1E01')
    #write_reg (serial_port, LDC1614_CONFIG, '0000')
    
    ldc_start_streaming(serial_port)

    try:
        while getattr(t, "do_run", True):   
            read_val = serial_port.read(32)
            #print("Read:%s" % (binascii.hexlify(read_val)))
            #get channel 0
            ch_0 = int(binascii.hexlify(read_val[7:11]), 16)
            AddValue(ch_0)
            #AddValue(ch_0, ch0_buf)
            #print("read:%s"%ch_0)
            #get channel 1
            ch_1 = int(binascii.hexlify(read_val[11:15]), 16)
            #AddValue(ch_1, ch1_buf)
            #get channel 2
            ch_2 = int(binascii.hexlify(read_val[15:19]), 16)
            #AddValue(ch_2, ch2_buf)
            #get channel 3
            ch_3 = int(binascii.hexlify(read_val[19:23]), 16)
            #AddValue(ch_3, ch3_buf)

            time.sleep(0.005)  # ~200Hz
    except ValueError:
        pass

    print('existing...')
    while serial_port.inWaiting():
        read_val = serial_port.read(serial_port.inWaiting())
        #print("Read:%s" % (binascii.hexlify(read_val)))

    ldc_stop_streaming(serial_port)
    serial_port.close()
    exit()


#############################################################################################

def main():
    #threading.Thread(target=msp430).start()
    t = threading.Thread(target=msp430)
    t.start()

    def handle_close(evt):
        t.do_run = False
        t.join()

    def reScale():
        range_max_temp = 0
        range_min_temp = 8800000000
        for itrd in ch0_buf:
            if range_max_temp < itrd:
                range_max_temp = itrd
            if range_min_temp > itrd:
                range_min_temp = itrd
        print("max: %s, min: %s" % (range_max_temp,range_min_temp))
        return [range_max_temp, range_min_temp] 

    def press(event):
        print('press', event.key)
        sys.stdout.flush()
        if event.key == 'r':  #rescale
            r_max, r_min = reScale()
            p1.set_ylim(r_min, r_max)
            p2.set_ylim(r_min, r_max)
            fig.canvas.draw()

        if event.key == 'i':  #zoom in
            r_min, r_max = p1.get_ylim()
            r_range = r_max - r_min
            r_adaption = r_range * 0.01
            p1.set_ylim(r_min+r_adaption, r_max-r_adaption)
            p2.set_ylim(r_min+r_adaption, r_max-r_adaption)
            fig.canvas.draw()

        if event.key == 'o':  #zoom out
            r_min, r_max = p1.get_ylim()
            r_range = r_max - r_min
            r_adaption = r_range * 0.1
            p1.set_ylim(r_min-r_adaption, r_max+r_adaption)
            p2.set_ylim(r_min-r_adaption, r_max+r_adaption)
            fig.canvas.draw()

        if event.key == 'w':   #shift up
            r_min, r_max = p1.get_ylim()
            r_range = r_max - r_min
            r_adaption = r_range * 0.1
            p1.set_ylim(r_min+r_adaption, r_max+r_adaption)
            p2.set_ylim(r_min+r_adaption, r_max+r_adaption)
            fig.canvas.draw()

        if event.key == 'x':   #shift down
            r_min, r_max = p1.get_ylim()
            r_range = r_max - r_min
            r_adaption = r_range * 0.1
            p1.set_ylim(r_min-r_adaption, r_max-r_adaption)
            p2.set_ylim(r_min-r_adaption, r_max-r_adaption)
            fig.canvas.draw()

    fig, (p1, p2) = plt.subplots(2, 1)
    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.mpl_connect('key_press_event', press)

    range_max = 0
    range_min = 8803000000

    #define y axis range based on 3 second sample collection
    t_end = time.time() + 10 #10 secs
    while time.time() < t_end:
        #print(ch0_buf[-1]) #peak at the latest element
        temp_ch0 = ch0_buf[-1]
        print("read: %s"%(temp_ch0))
        if range_max < temp_ch0: 
            range_max = temp_ch0
        if range_min > temp_ch0:
            range_min = temp_ch0

    print("max: %s, min: %s" % (range_max,range_min))

    print("==============")

    plot_data, = p1.plot(ch0_buf, animated=True)
    plot_processed, = p2.plot(ch1_buf, animated=True)
    p1.set_ylim(range_min, range_max)
    p2.set_ylim(range_min, range_max)
    
    def animate(i):
        plot_data.set_ydata(ch0_buf)
        plot_data.set_xdata(range(len(ch0_buf)))
        plot_processed.set_ydata(ch1_buf)
        plot_processed.set_xdata(range(len(ch1_buf)))
        return [plot_data, plot_processed]
    
    ani = animation.FuncAnimation(fig, animate, range(10000), 
                                  interval=50, blit=True)
    plt.show()

if __name__ == "__main__":
    main()