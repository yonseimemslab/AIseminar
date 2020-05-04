# ===============================================
# Sample code to receive measurements from LDC1000 inductance sensor, produce a sound and connetc to LEGO EV3
# Ekaterina Baibuz
# ===============================================

import time
import signal
import math

import ldc1000
import tools
import constants as const
import callback_sound

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
L_0 = 19.564
L_step = 0.01
keep_running = True
sleep_time = 10.0 # 10 second before runs
full_functional = True
sound_file = "/Volumes/Transcend/TSB/workshop/mihkel/science-basement/mac/smb_stage_clear.wav"
#sound_file = "/Volumes/Transcend/TSB/workshop/mihkel/science-basement/mac/mk64_mario09.wav"
# Initialize
if (full_functional):
    ldc1000.config()
#    fdc2214.config()
    #drdaq.init()
import paramiko
server = "192.168.3.2"
username = "robot"
password = "maker"
'''
ssh = paramiko.SSHClient()
cmd_to_execute = "python3 /home/robot/motor_movement/angle_example.py"
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server, username=username, password=password)
'''

imax = 30
L_min = math.inf
L_max = -math.inf
print("Calibrating for " + str(imax*0.1) + " seconds, please wait...")
for i in range(imax):
    # measure sensors
    if (full_functional):
        L = ldc1000.read_inductance()  # inductance [uH]
    else:
        L = tools.get_random()
    if (L < L_min): L_min = L
    if (L > L_max): L_max = L
    time.sleep(0.1)

L_0 = (L_max + L_min)/2
L_step = L_max - L_min

print("Calibration ready: L_0 = " + format_d(L_0) + ", L_step = " + format_d(L_step))
time.sleep(0.5)

print("L[uH],  Z[kOHm]")

# Loop; break the loop with a keystroke
while(keep_running):    
    # measure sensors
    if (full_functional):
        L = ldc1000.read_inductance()  # inductance [uH]
        Z = ldc1000.read_impedance()   # impedance [kOhm]
    else:
        
        L = tools.get_random()
        Z = tools.get_random()
    callback_sound
    # compose string to the console
    results = ""
    results += format_d(L)
    results += format_d(Z)
    print(results[1:])

    # give CPU some time before looping again
    # drivers need 0.01 sec for one measurement
    if ( math.fabs(L-L_0)>=L_step):        
        callback_sound.play(sound_file)
        
   #     ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
                
        #keep_running = False
        #time.sleep(sleep_time)
    time.sleep(0.1)
#ssh.close()
