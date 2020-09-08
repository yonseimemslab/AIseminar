import RPi.GPIO as gpio
import time

pin=21
gpio.setmode(gpio.BCM)
gpio.setup(pin,gpio.OUT)

p=gpio.PWM(pin,5000)
p.start(100)
n=50

try:
    while True:
        p.changeDutyCycle(n)

        print(n)

except KeyboardInterrupt:
    p.stop()
    gpio.cleanup()