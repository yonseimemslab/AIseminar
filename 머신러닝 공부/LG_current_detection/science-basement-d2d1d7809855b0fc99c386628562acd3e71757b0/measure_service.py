# ===============================================
# Sample code to receive measurements from LDC1000, FDC2214 and DrDaq modules
# (c) 2017 Mihkel Veske
# ===============================================

import time
import signal
import math

import fdc2214
#import ldc1000
import drdaq
import tools
import constants as const

# ===============================================
# === Some simple macros
# ===============================================

# apply formatting for measured values
def format_d(value):
    return ", %.3f" % value
    
def format_f(value):
    return ", %.1f" % value
    
def format_i(value):
    return ", %d" % value    

# key-listener for ctrl+c
def signal_handler(signum, stack):
    global keep_running
    keep_running = False

# ===============================================
# === Code itself
# ===============================================

signal.signal(signal.SIGINT, signal_handler)
keep_running = True
full_functional = True

print("light, T[degC], C[pF], dC[pF], L[uH],  Z[kOHm], red, green, blue")

# Initialize
if (full_functional):
    #ldc1000.config()
    fdc2214.config()
    #drdaq.init()

# Loop; break the loop with a keystroke
while(keep_running):
    #light = T = C = dC = L = Z = 0    
    T_correction = -5.1 # difference between on-wire and on-board temperature sensors
    
    # measure sensors
    if (full_functional):
        #light = drdaq.get_light()      # light intensity [%]
        #T = drdaq.get_ext1()  # temperature [degC]
        #T = max(drdaq.get_ext1(), drdaq.get_temperature()+T_correction)  # temperature [degC]
        C = fdc2214.read_ch0()        # capacitance [pF]
        #dC = fdc2214.read_ch10()      # capacitance diffrence [pF]
        #L = ldc1000.read_inductance()  # inductance [uH]
        #Z = ldc1000.read_impedance()   # impedance [kOhm]
    else:
        #light = tools.get_random()
        T = tools.get_random()
        C = tools.get_random()
        dC = tools.get_random()
        #L = tools.get_random()
        #Z = tools.get_random()

    # encode temperature, inductance and impedance into LED RGB values
    red = min(255, max(0, math.exp(T * 0.22) - 210))
    #green = min(255, math.exp(L * 0.26))
    green =  255 * light / 100
    #blue = min(255, math.exp(Z * 0.44))
    blue = 0
    drdaq.set_led(int(red), int(green), int(blue))
    
    # compose string to the console
    results = ""
    results += format_f(light)
    results += format_f(T)
    results += format_d(C)
    results += format_d(dC)
    #results += format_d(L)
    #results += format_d(Z)
    results += format_i(red)
    results += format_i(green)
    results += format_i(blue)
    
    # output data
    print(results[1:])

    # give CPU some time before looping again
    # drivers need 0.01 sec for one measurement
    time.sleep(0.1)
