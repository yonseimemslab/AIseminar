import serial
import random as rnd

class SerialDevice:
    '''
    General class to control serial device
    '''

    def __init__(self, baud_rate=0, port_name="", device_name=""):
        "open serial port"

        if (baud_rate == 0): return
        try:
            self.ser = serial.Serial(
                port=port_name, baudrate=baud_rate,
                parity=serial.PARITY_NONE, timeout=1,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS)
            if (not self.ser.isOpen()):
                self.ser.open()

            self.unit_disabled = False

        except serial.SerialException:
            print("-- Unable to open " + device_name + ". Activating random number generator.")
            self.unit_disabled = True

    def close(self):
        "close serial port"
        if (not self.unit_disabled):
            self.ser.close()

    def get_random(self, minimum=0.0, amplitude=1.0):
        "get random number with specified minimum and amplitude value"
        return minimum + amplitude * rnd.random()
