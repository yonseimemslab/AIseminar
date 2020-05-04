# ===============================================
# Driver for LDC1000 inductance-impedance to digital module
# (c) 2017 Mihkel Veske
# ===============================================

import serial
import time
import numpy as np

import constants as const
import tools

#===========================================================
# USB CDC commands
READ = '03'
WRITE = '02'
STREAM_ON = '06'
STREAM_OFF = '07'
FIRMWARE ='09'

#===========================================================
# LDC1000 addressing space
DevID       = '00'
RpMax       = '01'
RpMin       = '02'
SensorFreq  = '03'
LdcConfic   = '04'
ClkConfig   = '05'
ThresHiLSB  = '06'
ThresHiMSB  = '07'
ThresLoLSB  = '08'
ThresLoMSB  = '09'
IntConfig   = '0A'
PwrConfig   = '0B'
Status      = '20'
ProxDataLSB = '21'
ProxDataMSB = '22'
FreqDataLSB = '23'
FreqDataMID = '24'
FreqDataMSB = '25'

#===========================================================
# LDC1000 internal variables
serial_port = serial.Serial()

#===========================================================

# Convert proximity data at addresses 0x21 & 0x22 to sensor impedance
def prox2impedance(data):
    Y = 1.0 * data / 2**15
    Rp_max = 83.111 # upper limit of resonant impedance input range specified by register 0x01 [kOhm]
    Rp_min = 2.394  # lower limit of resonant impedance input range specified by register 0x02 [kOhm]
    Rp = (Rp_max*Rp_min) / (Rp_min*(1-Y) + Rp_max*Y) # resonant impedance [kOhm]
    return round(Rp, 3)

# Convert frequency counter value at addresses 0x23,0x24,0x25 to sensor inductance 
def freq2inductance(data):
    Fext = 6.0     # frequency of the external clock or crystal [MHz]
    C = 100.0      # parallel capacitance of the resonator [pF]
    t_resp = 6144  # response time in register 0x04
    
    if data == 0: return 0.0
    
    f_sensor = (Fext / data) * (t_resp / 3.0) # sensor frequency [MHz]   
    L = 1e6 / (C * (2*np.pi*f_sensor)**2)     # sensor inductance [uH]
    return round(L, 3) 

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

    except serial.SerialException:
        print ("Error writing to LCD1000 in", serial_port.port)

# write value to register
def write_reg(reg, data):
    send_data = WRITE + reg + data + '00';
    write_data(send_data)
    
# read value from register
def read_reg(reg):
    global serial_port
    
    send_data = READ + reg + '0000';
    if (const.PRINT_TX_DATA):
        print ("Sent:", send_data)
    
    try:
        # clean input buffer
        serial_port.read(serial_port.inWaiting())
        
        # order data from ldc1000
        serial_port.write(send_data.encode('utf-8'))
        
        # wait for the response
        while (serial_port.inWaiting() < 32):
            time.sleep(0.01)
        
        # acquire data
        data = serial_port.read(serial_port.inWaiting())
        if (const.PRINT_RX_DATA):
            print ("Read:", end='')
            for d in data: print (" %d"%d, end='')
            print()
            
        return data[8]
        
    except serial.SerialException:
        print ("Error reading LCD1000 register", reg, "at port", serial_port.port)
        return 0

# open serial port and initialise LDC1000 registers
def config():
    global serial_port
    
    # open serial port
    serial_port = tools.get_serial(const.LDC1000_PORT, 9600);
    if (not serial_port.isOpen()):
        serial_port.open()
        
    write_reg(RpMax,       '0E')
    write_reg(RpMin,       '3B')
    write_reg(SensorFreq,  '94')
    write_reg(LdcConfic,   '17')
    write_reg(ClkConfig,   '02')
              
    write_reg(ThresHiLSB,  '50')
    write_reg(ThresHiMSB,  '14')
    write_reg(ThresLoLSB,  'C0')
    write_reg(ThresLoMSB,  '12')
              
    write_reg(IntConfig,   '04')
   
# start continuous streaming 
def start_stream():
    send_data = STREAM_ON + ProxDataLSB + '0000';
    write_data(send_data)

# stop continuous streaming 
def stop_stream():
    send_data = STREAM_OFF + ProxDataLSB + '0000';
    write_data(send_data)  

# measure sensor inductance
def read_inductance():     
    freq_msb = read_reg(FreqDataMSB)
    freq_mid = read_reg(FreqDataMID)
    freq_lsb = read_reg(FreqDataLSB)
    return freq2inductance(65536*freq_msb + 256*freq_mid + freq_lsb)
    
# measure sensor impedance
def read_impedance():
    prox_msb = read_reg(ProxDataMSB)
    prox_lsb = read_reg(ProxDataLSB)
    return prox2impedance(256*prox_msb + prox_lsb)    
        
# read impedance and inductance stream
def read_stream():
    global serial_port
    try:       
        # wait until sufficient amount of data is available
        while (serial_port.inWaiting() < 2048):
            time.sleep(0.1)
        
        in_waiting = serial_port.inWaiting()    
        data_str = serial_port.read(in_waiting)
                       
        data = []
        for d in data_str:
            data.append(ord(d))
            
        d1 = d2 = d3 = d4 = 0
        if (in_waiting == 2048 or in_waiting == 4095):
            d1 = np.mean(data[0:1024:2])
            d2 = np.mean(data[1:1024:2])
            d3 = np.mean(data[1024:2048:2])
            d4 = np.mean(data[1025:2048:2])
        elif (in_waiting == 2049):
            d1 = np.mean(data[1:1025:2])
            d2 = np.mean(data[2:1025:2])
            d3 = np.mean(data[1025:2049:2])
            d4 = np.mean(data[1026:2049:2])
        
        return [prox2impedance(256*d1 + d2), freq2inductance(256*d3 + d4)]
        
    except serial.SerialException:
        print ("Error reading LCD1000 in", serial_port.port)
        return [0, 0]
