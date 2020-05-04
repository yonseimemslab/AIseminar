# _*_ coding: utf-8 _*_
from MSP430 import MSPComm
import socket
import time
import threading
import serial.tools.list_ports
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def serialRead():
    serialDict = []
    serialNum = 0
    ports = list(serial.tools.list_ports.comports())
    for a, b, c in ports:
        # print(a,b,c)
        d = a.split('.')
        if d[-1] != 'Bluetooth-Incoming-Port':
            # print (d[-1])
            serialDict.append(a)
            serialNum += 1
    return serialNum, serialDict


class FetchData:
    def __init__(self, msp):
        self.msp = msp
        # second
        self.send_time = 0.1
        # need to renew everytime
        self.data = []
        self.datanumers = 0
        self.sumcoils = 16
        self.row = 4
        self.column = self.sumcoils/self.row
        self.Id=[]

    def sender(self):
        while 1:
            ch = self.fetch_ch_data()
            self.datanumers = self.datanumers + 1
            #self.Id.append(self.datanumers)
            # print ch
            #self.mysocket.send(' '.join(str(e) for e in ch) + "\n")
            ch.append(self.datanumers)
            self.data.append(ch)
            # self.mysocket.send('100' + '\n')

            time.sleep(self.send_time)

    def drawimage(self):
        # plt.figure(figsize=(8,8))
        plt.figure()
        plt.ion()
        while 1:
            singlecoildata = np.array(self.data[-50:])

            for r in range(1):
                for c in range(self.column):
                    axi = plt.subplot2grid((self.row, self.column), (r, c), colspan=1, rowspan=1)
                    axi.plot(singlecoildata[:, -1], singlecoildata[:, self.column * r + c],'r')  # can be replaced by my function
            axi.cla()
            plt.pause(0.01)

    def fetch_ch_data(self):
        ch = [0] * self.sumcoils
        for i in range(10):  # extract 10 samples and then calculate the average each time.
            for j in range(self.sumcoils):
                ch[j] += (self.msp[j / self.column].data_ch[j % self.column] - self.msp[j / self.column].base_ch[j % self.column]) / 10
            time.sleep(0.001)
        return ch

    def start(self):
        t = threading.Thread(target=self.sender, args=())
        t.start()
        realimage = threading.Thread(target=self.drawimage, args=())
        realimage.start()


if __name__ == "__main__":
    mymsp = list()

    serialNums, serialDicts = serialRead()
    serialDicts.sort()
    print(serialNums, serialDicts)
    serialID = 0
    for COM in serialDicts:
        serialID += 1
        mymsp.append(MSPComm(COM, str(serialID)))

    fetchdata = FetchData(mymsp)
    fetchdata.start()
