
'''
Classes to control Widgetlords modules
https://widgetlords.com/blogs/news/the-pi-spi-series-is-complete

Those classes require libwidgetlords to be preinstalled.
The guide for this can be found from
https://widgetlords.com/pages/getting-started-with-pi-spi-libraries
'''

import widgetlords.pi_spi as pi_spi
import widgetlords

class PiSpi_8KO():
    '''
    Class to control WidgetLords Electronics Raspberry Pi Relay Output Module
    https://widgetlords.com/products/pi-spi-8ko-raspberry-pi-relay-output-interface
    '''
    def __init__(self, alt_channel: bool = False):
        "Initialize PiSpi_8KO device"
        pi_spi.init()
        self.device = pi_spi.Mod8KO(alt_channel)

    def write(self, data: int):
        "Activate desired relays"
        self.device.write(data)

    def write_single(self, channel: int, data: int):
        "Activate single relay"
        if (channel < 0 or channel > 7):
            print ("Invalid channel:", channel)
            return
        self.device.write_single(channel, data)

class PiSpi_8AI():
    '''
    Class to control WidgetLords Electronics Raspberry Pi Analog Input Module
    https://widgetlords.com/products/pi-spi-8ai-raspberry-pi-analog-input-interface
    '''

    current_min_mA = 4       # current min scale = 0 or 4 mA
    current_max_mA = 20      # current full scale = 20 mA
    current_min_adc = 745
    current_max_adc = 3723   # AD Counts to equal 20 mA (20 mA into 150Ohms = 3 Vdc / 3.3 Vdc full scale * 4096 Counts)

    voltage_min = 0
    voltage_max = 6.6        # voltage full scale = 6.6 VDC
    voltage_min_adc = 0
    voltage_max_adc = 4095   # AD Counts to equal 6.6 VDC

    r_temp = 10000        # the Thermistor Ohms at Room Temperature (25 Deg.C) 
    beta = 3380           # the Beat value of the Thermistor being used
    max_ad_counts = 4095  # the maximum ad counts ie: 4095 for a 12 bit A/D converter
    
    def __init__(self, alt_channel: bool = False):
        "Initialize PiSpi_8AI device"
        pi_spi.init()
        self.device = pi_spi.Mod8AI(alt_channel)

    def read_adc(self, channel: int):
        "Read raw ADC data from channel"
        if (channel < 0 or channel > 7):
            print ("Invalid channel:", channel)
            return -1
        return self.device.read_single(channel)  

    def read_current(self, channel: int):
        "Read current value in mA from a channel"
        if (not 0 <= channel <= 3):
            print ("Invalid channel: %d" % channel)
            return -1

        adc = self.device.read_single(channel)
        return widgetlords.counts_to_value(adc, self.current_min_adc, 
            self.current_max_adc, self.current_min_mA, self.current_max_mA)

    def read_voltage(self, channel: int):
        "Read voltage value in volts from a channel"
        if (not 4 <= channel <= 7):
            print ("Invalid channel: %d" % channel)
            return -1
        
        adc = self.device.read_single(channel)
        return widgetlords.counts_to_value(adc, self.voltage_min_adc, 
            self.voltage_max_adc, self.voltage_min, self.voltage_max)

    def read_temperature(self, channel: int):
        "Read temperature value in deg C from a channel"
        if (not 0 <= channel <= 7):
            print ("Invalid channel: %d" % channel)
            return -1
        
        adc = self.device.read_single(channel)
        return widgetlords.steinhart_hart(self.r_temp, self.beta, self.max_ad_counts, adc)
