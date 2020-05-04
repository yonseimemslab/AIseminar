#this file is used for read serial number
import serial.tools.list_ports
ports=list(serial.tools.list_ports.comports())
serialNum=0
serialDict=[]
for a,b,c in ports:
    print(a,b,c)
    d = a.split('.')
    if d[-1]!='Bluetooth-Incoming-Port':
        #print (d[-1])
        serialDict.append(a)
        serialNum+=1
print (serialDict)
print (serialNum)