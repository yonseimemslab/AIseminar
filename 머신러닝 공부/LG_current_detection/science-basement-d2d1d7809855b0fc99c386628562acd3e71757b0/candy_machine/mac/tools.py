import sys
import serial
import random as rnd

if sys.version_info[0] == 3:
    from urllib.request import urlopen
    import urllib.request
else:
    from urllib import urlopen
    import urllib

import constants as const

# store the temperature to Wolfram Data Drop
def write_datadrop(T, C):
    if (T == 0 or C == 0):
        return
    url = "https://datadrop.wolframcloud.com/api/v1.0/Add?bin=" + const.databin_id
    url += "&T=%.3f&C=%.3f" % (T, C)
    try:
        urlopen(url)
    except urllib.error.HTTPError as err:
        print (err)


# generate serial port object
def get_serial(port_name, baud_rate):
    try:
        ser = serial.Serial(
            port=port_name, baudrate=baud_rate,
            parity=serial.PARITY_NONE, timeout=1,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        return ser
    except serial.SerialException:
        print ("Error: port ", port_name, " not found!")
        return 0

# get random number with specified minimum and amplitude value
def get_random(minimum=0.0, amplitude=1.0):
    return minimum + amplitude * rnd.random()
