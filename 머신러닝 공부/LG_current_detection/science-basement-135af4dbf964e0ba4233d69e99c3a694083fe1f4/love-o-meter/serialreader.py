
import serial
import time

class SerialReader():
    def __init__(self, baud_rate, port_name):
        self.ser = serial.Serial(
            port=port_name, baudrate=baud_rate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        
        if not self.ser.isOpen():
            self.ser.open()
        
    def read_line(self):
        line = self.ser.readline()
        return float(line[:-2])
        
    def write_line(self, data):
        self.ser.write(str.encode(data+'\n'))
                
    def read_byte(self):
        return self.ser.read(1)
        
    def close(self):
        self.ser.close()