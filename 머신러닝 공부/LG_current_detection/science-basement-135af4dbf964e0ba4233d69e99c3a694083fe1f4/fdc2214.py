# ===============================================
# Driver for FDC2214 capacitance to digital module
# (c) 2017 Mihkel Veske
# ===============================================

import serial
import time
import numpy as np

import constants as const
import tools

#===========================================================
# USB CDC commands
WRITE = '36'
READ = '37'
STREAM_ON = '32'
STREAM_OFF = '33'
FIRMWARE ='4C'

#===========================================================
# FDC2214 addressing space
DataMSB_CH0  = '00'
DataLSB_CH0  = '01'
DataMSB_CH1  = '02'
DataLSB_CH1  = '03'
DataMSB_CH2  = '04'
DataLSB_CH2  = '05'
DataMSB_CH3  = '06'
DataLSB_CH3  = '07'

Rcount_CH0   = '08'
Rcount_CH1   = '09'
Rcount_CH2   = '0A'
Rcount_CH3   = '0B'
Offset_CH0   = '0C'
Offset_CH1   = '0D'
Offset_CH2   = '0E'
Offset_CH3   = '0F'
SetCount_CH0 = '10'
SetCount_CH1 = '11'
SetCount_CH2 = '12'
SetCount_CH3 = '13'
ClockDiv_CH0 = '14'
ClockDiv_CH1 = '15'
ClockDiv_CH2 = '16'
ClockDiv_CH3 = '17'
DriveCur_CH0 = '1E'
DriveCur_CH1 = '1F'
DriveCur_CH2 = '20'
DriveCur_CH3 = '21'

Status       = '18'
ErrorConfig  = '19'
Config       = '1A'
MuxConfig    = '1B'
Reset        = '1C'
DevID        = '7F'

#===========================================================
# FDC2214 internal variables
serial_port = serial.Serial()

#===========================================================

# convert raw measurement data into capacitance
# sensor capacitance C_sensor = 1 / L*(2*pi*f_sensor)^2 - C 
# and sensor frequency f_sensor = data * f_ref / 2^28
def data2cap(data):
    f_ref = 40.0 # reference frequency [MHz]
    C = 33.0     # parallel sensor capacitance [pF]
    L = 18.0     # parallel sensor inductance [uH]
    
    reading = int(data, 16) # convert hex string to decimal integer   
    f_sensor = reading * f_ref / 2**28   # sensor frequency [MHz]
    C_sensor = 0.0                       # sensor capacitance [pF]
    if f_sensor > 0: C_sensor = 1e6 / (L * (2*np.pi*f_sensor)**2) - C 
    return round(C_sensor, 3)

# read the capacitance in channel 0
def read_ch0():
    [C0, C1, C2, C3] = get_data()
    return C0;

# read the capacitance in channel 1
def read_ch1():
    [C0, C1, C2, C3] = get_data()
    return C1;

# read the capacitance difference between channel 1 and channel 0
def read_ch10():
    [C0, C1, C2, C3] = get_data()
    return C1 - C0;
    
# read the capacitance difference in channel 2
def read_ch2():
    [C0, C1, C2, C3] = get_data()
    return C3 - C2;
    
# read measured capacitances
def get_data():
    global serial_port
    
    send_data = '1000'
    if (const.PRINT_TX_DATA):
        print ("Sent:", send_data)
        
    try:
        # Read pending input bytes
        while (serial_port.inWaiting() > 0):
            serial_port.read(serial_port.inWaiting())

        # Send data
        serial_port.write(send_data.encode("utf-8"))
        
        # wait for the response
        #while (serial_port.inWaiting() < 32): time.sleep(0.1)
        time.sleep(0.01)
        
        # read the response
        response = serial_port.read(serial_port.inWaiting())
        if (const.PRINT_RESPONSE_DATA):
            print ("Response:", end='')
            for r in response: print (" %d" % r, end='')
            print()
            
        # convert readings in hex string format into integers
        if len(response) >= 36:
            return [data2cap(response[0:8]), data2cap(response[9:17]),
            data2cap(response[18:26]), data2cap(response[27:35])]

    except serial.SerialException:
        print ("Error writing to FDC2214 in", serial_port.port)

    return [0,0,0,0]

# open serial port and initialise FDC2214 registers
def config():
    global serial_port
    
    # open serial port
    serial_port = tools.get_serial(const.FDC2214_PORT, 115200);
    if (not serial_port.isOpen()):
        serial_port.open()
    
    return

# write data string 
def write_data(data):
    global serial_port
    
    if (const.PRINT_TX_DATA):
        print ("Sent:", data)
        
    try:
        # Read pending input bytes
        while (serial_port.inWaiting() > 0):
            serial_port.read(serial_port.inWaiting())

        # Send data
        serial_port.write(data.encode("utf-8"))
        
        # wait for the response
        while (serial_port.inWaiting() < 32):
            time.sleep(0.1)
        
        # read the response
        response = serial_port.read(serial_port.inWaiting())
        if (const.PRINT_RESPONSE_DATA):
            print ("Response:", end='')
            for r in response: print (" %d" % r, end='')
            print()
        return response[8];

    except serial.SerialException:
        print ("Error writing to FDC2214 in", serial_port.port)
    
    return 0

# read value from register
def read_reg(reg):
    send_data = LDC_READ + reg + '00'
    return write_data(send_data);
        
# write value to register
def write_reg(reg, write_data):
    send_data = LDC_WRITE + reg + write_data + '00'
    write_data(send_data);
