#############################################################################################
# Author: Jun Gong
# Function: Fetch Data from 4 by 4 coil matrix
# Date: 05/07/2018
#############################################################################################


from MSP430 import MSPComm
import socket
import time
import threading
import serial.tools.list_ports

numofCoils = 30

def serialRead():
    serialDict=[]
    serialNum=0
    ports=list(serial.tools.list_ports.comports())
    for a,b,c in ports:
        #print(a,b,c)
        d = a.split('.')
        if d[-1]!='Bluetooth-Incoming-Port':
            #print (d[-1])
            serialDict.append(a)
            serialNum+=1
    return serialNum,serialDict

class FetchData:
    def __init__(self, msp):
        self.msp = msp
        # second
        self.send_time = 0.1
        self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mysocket.connect(("localhost", 8002))

    def sender(self):
        while 1:
            ch = self.fetch_ch_data()
            #print ch
            self.mysocket.send(' '.join(str(e) for e in ch) + "\n")

            #self.mysocket.send('100' + '\n')

            time.sleep(self.send_time)

    def fetch_ch_data(self):
        ch = [0] * 16
        for i in range(10):#extract 10 samples and then calculate the average each time.
            for j in range(16):
                ch[j] += (self.msp[j/4].data_ch[j%4] - self.msp[j/4].base_ch[j%4]) / 10
            time.sleep(0.001)
        return ch

    def start(self):
        t = threading.Thread(target=self.sender, args=())
        t.start()


if __name__ == "__main__":
    mymsp = list()

    serialNums ,serialDicts = serialRead()
    serialDicts.sort()
    #print serialNums,serialDicts
    serialID=0
    for COM in serialDicts:
        serialID+=1
        mymsp.append(MSPComm(COM, str(serialID)))


    fetchdata = FetchData(mymsp)
    fetchdata.start()