import serial
import time
import numpy as np

from serial_device import *

class FDC2214(SerialDevice):
    '''
    Driver class to control FDC2214 capacitance to digital evaluation module
    The datasheet of FDC2214 chip and its EVM can be found from
    http://www.ti.com/lit/ds/symlink/fdc2214.pdf
    http://www.ti.com/lit/ug/snou138a/snou138a.pdf
    '''
    
    #===========================================================
    # Serial debug flags
    PRINT_TX_DATA = 0
    PRINT_RX_DATA = 0
    PRINT_RESPONSE_DATA = 0

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
    def __init__(self, baud_rate, port_name):
        "open serial port and initialise FDC2214 registers"

        SerialDevice.__init__(self, baud_rate, port_name, "FDC2214")
        if (self.unit_disabled): return

        '''        
        self.write_reg(self.SetCount_CH0, '0400')
        self.write_reg(self.SetCount_CH1, '0400')
        self.write_reg(self.ClockDiv_CH0, '1001')
        self.write_reg(self.ClockDiv_CH1, '1001')
        self.write_reg(self.ErrorConfig,  '0001')
        self.write_reg(self.Config,       '1E01')
        self.write_reg(self.MuxConfig,    '820C')
        '''    

    def read_ch1(self):
        "read the capacitance difference in channel 1"
        if (self.unit_disabled): return self.get_random()
        
        [C0, C1, C2, C3] = self.get_data()
        return C1 - C0
        
    def read_ch2(self):
        "read the capacitance difference in channel 2"
        if (self.unit_disabled): return self.get_random()

        [C0, C1, C2, C3] = self.get_data()
        return C3 - C2
        
    def get_data(self):
        "read measured capacitances"
        
        send_data = '1000'
        if (self.PRINT_TX_DATA):
            print ("Sent:", send_data)
            
        try:
            # Read pending input bytes
            while (self.ser.inWaiting() > 0):
                self.ser.read(self.ser.inWaiting())

            # Send data
            self.ser.write(send_data.encode("utf-8"))
            
            # wait for the response
            #while (self.ser.inWaiting() < 32): time.sleep(0.1)
            time.sleep(0.1)
            
            # read the response
            response = self.ser.read(self.ser.inWaiting())
            if (self.PRINT_RESPONSE_DATA):
                print ("Response:", end='')
                for r in response: print (" %d" % r, end='')
                print()
                
            # convert readings in hex string format into integers
            if len(response) >= 36:
                return [self.data2cap(response[0:8]), self.data2cap(response[9:17]),
                        self.data2cap(response[18:26]), self.data2cap(response[27:35])]

        except serial.SerialException:
            print ("Error writing to FDC2214 in", self.ser.port)

        return [0,0,0,0]

    def data2cap(self, data):
        '''
        convert raw measurement data into capacitance
        sensor capacitance C_sensor = 1 / L*(2*pi*f_sensor)^2 - C 
        and sensor frequency f_sensor = data * f_ref / 2^28
        '''
        f_ref = 40.0 # reference frequency [MHz]
        C = 33.0     # parallel sensor capacitance [pF]
        L = 18.0     # parallel sensor inductance [uH]
        
        reading = int(data, 16) # convert hex string to decimal integer   
        f_sensor = reading * f_ref / 2**28   # sensor frequency [MHz]
        C_sensor = 0.0                       # sensor capacitance [pF]
        if f_sensor > 0: C_sensor = 1e6 / (L * (2*np.pi*f_sensor)**2) - C 
        return round(C_sensor, 2)

    def write_data(self, data):
        "write data string to unit"
        if (self.PRINT_TX_DATA):
            print ("Sent:", data)
            
        try:
            # Read pending input bytes
            while (self.ser.inWaiting() > 0):
                self.ser.read(self.ser.inWaiting())

            # Send data
            self.ser.write(data.encode("utf-8"))
            
            # wait for the response
            while (self.ser.inWaiting() < 32):
                time.sleep(0.1)
            
            # read the response
            response = self.ser.read(self.ser.inWaiting())
            if (self.PRINT_RESPONSE_DATA):
                print ("Response:", end='')
                for r in response: print (" %d" % r, end='')
                print()
            return response[8];

        except serial.SerialException:
            print ("Error writing to FDC2214 in", self.ser.port)
        
        return 0

    def read_reg(self, reg):
        "read value from register"
        send_data = self.LDC_READ + reg + '00'
        return self.write_data(send_data)

    def write_reg(self, reg, write_data):
        "write value to register"
        send_data = self.LDC_WRITE + reg + write_data + '00'
        self.write_data(send_data)
