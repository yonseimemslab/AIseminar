


#data = struct.pack(hex, 0x7E, 0xFF, 0x03, 0x00, 0x01, 0x00, 0x02, 0x0A, 0x01, 0xC8,      0x04, 0xD0, 0x01, 0x02, 0x80, 0x00, 0x00, 0x00, 0x00, 0x8E, 0xE7, 0x7E)
#while True :


#ser6.close()

import time

from keras.models import Sequential
import numpy as np
from keras.layers.core import Dense,Dropout
import keras
import h5py
import tensorflow
import serial
import struct
from sht_sensor import Sht
import datetime
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import subprocess
import sys


dt = pd.read_csv('/home/omni/Desktop/sht-sensor/scaler_2019-11-25-13-19_0910_1110_rh_notime.csv', index_col=0)
scaler=MinMaxScaler(copy=True,feature_range=(0,1))
dataset=dt.values
X=dataset[:,0:3]
scaler.fit(X)

model = Sequential()
model.add(Dense(25,input_dim=3, activation='relu'))
model.add(Dense(25,activation='relu'))
model.add(Dense(25,activation='relu'))
model.add(Dense(1))

model.load_weights("/home/omni/Desktop/sht-sensor/2019-11-25-13-19_0910_1110_rh_notime")

model1 = Sequential()
model1.add(Dense(25,input_dim=3, activation='relu'))
model1.add(Dense(25,activation='relu'))
model1.add(Dense(25,activation='relu'))
model1.add(Dense(1))

model1.load_weights("/home/omni/Desktop/sht-sensor/2019-11-25-13-19_0910_1110_rh_notime") 

from tkinter import *
from tkinter.font import Font
from keras import metrics
from itertools import chain
import time
from keras.models import Sequential
import numpy as np
from keras.layers.core import Dense,Dropout
import keras
import h5py
import tensorflow
import serial
import struct
from sht_sensor import Sht
import datetime
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import subprocess
import sys

tk=Tk()
w, h = tk.winfo_screenwidth(), tk.winfo_screenheight()
tk.geometry("1280x800")

leftFrame = LabelFrame(tk, text='Dust Data', font=('Times New Roman',23), width=50, height = 4)
leftFrame.grid(row=0,column=0,padx=10,pady=10)
l7=Label(leftFrame, text="PM 2.5",font=('Times New Roman',30), width=25,height=4, relief=RIDGE)
l7.grid(row=0,column=0,sticky=NSEW,padx=5, pady=10)

gasFrame=LabelFrame(tk, text='Gas Data(ppb)', font=('Times New Roman',23), width= 50, height = 12)
gasFrame.grid(row=1, column=0, padx=5, pady=7)

l1=Label(gasFrame, text="CO",font=('Times New Roman',30,'bold'),width=25,height=1, relief=RIDGE)
l1.grid(row=1,column=0,sticky=NSEW,padx=5, pady=8)   
l2=Label(gasFrame, text="SO2",font=('Times New Roman',30,'bold'),width=25,height=1,relief=RIDGE)
l2.grid(row=2,column=0,sticky=NSEW,padx=5, pady=8)   
l4=Label(gasFrame,text="TVOC",font=('Times New Roman',30,'bold'),width=25,height=1,relief=RIDGE)
l4.grid(row=3,column=0,sticky=NSEW,padx=5, pady=8)   
l5=Label(gasFrame,text="NO2",font=('Times New Roman',30,'bold'),width=25,height=1, relief=RIDGE)
l5.grid(row=4,column=0,sticky=NSEW,padx=5, pady=8)   
l6=Label(gasFrame,text="O3",font=('Times New Roman',30,'bold'),width=25,height=1,relief=RIDGE)
l6.grid(row=5,column=0,sticky=NSEW,padx=1, pady=8)

otherFrame=LabelFrame(tk,text='Temp/Humid', font=('Times New Roman',23), width=12, height= 6)
otherFrame.grid(row=0,column=1,padx=5,pady=20)








class PMS7003(object):
  n=0
  g=0
  t=[]
  p=[]
  #sht = Sht(3,2)
  # PMS7003 protocol data (HEADER 2byte + 30byte)
  PMS_7003_PROTOCOL_SIZE = 32

  # PMS7003 data list
  HEADER_HIGH            = 0  # 0x42
  HEADER_LOW             = 1  # 0x4d
  FRAME_LENGTH           = 2  # 2x13+2(data+check bytes)
  DUST_PM1_0_CF1         = 3  # PM1.0 concentration unit μ g/m3（CF=1，standard particle）
  DUST_PM2_5_CF1         = 4  # PM2.5 concentration unit μ g/m3（CF=1，standard particle）
  DUST_PM10_0_CF1        = 5  # PM10 concentration unit μ g/m3（CF=1，standard particle）
  DUST_PM1_0_ATM         = 6  # PM1.0 concentration unit μ g/m3（under atmospheric environment）
  DUST_PM2_5_ATM         = 7  # PM2.5 concentration unit μ g/m3（under atmospheric environment）
  DUST_PM10_0_ATM        = 8  # PM10 concentration unit μ g/m3  (under atmospheric environment)
  DUST_AIR_0_3           = 9  # indicates the number of particles with diameter beyond 0.3 um in 0.1 L of air.
  DUST_AIR_0_5           = 10 # indicates the number of particles with diameter beyond 0.5 um in 0.1 L of air.
  DUST_AIR_1_0           = 11 # indicates the number of particles with diameter beyond 1.0 um in 0.1 L of air.
  DUST_AIR_2_5           = 12 # indicates the number of particles with diameter beyond 2.5 um in 0.1 L of air.
  DUST_AIR_5_0           = 13 # indicates the number of particles with diameter beyond 5.0 um in 0.1 L of air.
  DUST_AIR_10_0          = 14 # indicates the number of particles with diameter beyond 10 um in 0.1 L of air.
  RESERVEDF              = 15 # Data13 Reserved high 8 bits
  RESERVEDB              = 16 # Data13 Reserved low 8 bits
  CHECKSUM               = 17 # Checksum code


  # header check
  def header_chk(self, buffer):

    if (buffer[self.HEADER_HIGH] == 66 and buffer[self.HEADER_LOW] == 77):
      return True

    else:
      return False

  # chksum value calculation
  def chksum_cal(self, buffer):

    buffer = buffer[0:self.PMS_7003_PROTOCOL_SIZE]

    # data unpack (Byte -> Tuple (30 x unsigned char <B> + unsigned short <H>))
    chksum_data = struct.unpack('!30BH', buffer)

    chksum = 0

    for i in range(30):
      chksum = chksum + chksum_data[i]

    return chksum

  # checksum check
  def chksum_chk(self, buffer):

    chk_result = self.chksum_cal(buffer)

    chksum_buffer = buffer[30:self.PMS_7003_PROTOCOL_SIZE]
    chksum = struct.unpack('!H', chksum_buffer)

    if (chk_result == chksum[0]):
      return True

    else:
      return False

  # protocol size(small) check
  def protocol_size_chk(self, buffer):

    if(self.PMS_7003_PROTOCOL_SIZE <= len(buffer)):
      return True

    else:
      return False

  # protocol check
  def protocol_chk(self, buffer):

    if(self.protocol_size_chk(buffer)):

      if(self.header_chk(buffer)):

        if(self.chksum_chk(buffer)):

          return True
        else:
          print("Chksum err")
      else:
        print("Header err")
    else:
      print("Protol err")

    return False

  # unpack data
  # <Tuple (13 x unsigned short <H> + 2 x unsigned char <B> + unsigned short <H>)>
  def unpack_data(self, buffer):

    buffer = buffer[0:self.PMS_7003_PROTOCOL_SIZE]

    # data unpack (Byte -> Tuple (13 x unsigned short <H> + 2 x unsigned char <B> + unsigned short <H>))
    data = struct.unpack('!2B13H2BH', buffer)

    return data


  def print_serial(self, buffer):
    sht = Sht(3,2)
    s=datetime.datetime.now()
    #self.n+=1
    chksum = self.chksum_cal(buffer)
    data = self.unpack_data(buffer)
    a=data[self.DUST_PM1_0_CF1]
    b=data[self.DUST_PM1_0_ATM]
    c=data[self.DUST_PM2_5_CF1]
    d=data[self.DUST_PM2_5_ATM]
    e=data[self.DUST_PM10_0_CF1]
    f=data[self.DUST_PM10_0_ATM]
    g=data[self.DUST_AIR_0_3]
    h=data[self.DUST_AIR_0_5]
    i=data[self.DUST_AIR_1_0]
    j=data[self.DUST_AIR_2_5]
    k=data[self.DUST_AIR_5_0]
    l=data[self.DUST_AIR_10_0]
    #print(s,a,b,c,d,e,f,g,h,i,j,k,l)
    self.input_parameter=[d,round(sht.read_t(),3),round(sht.read_rh(),3)]
    self.input_parameter=np.array([self.input_parameter])
    self.input_parameter=scaler.transform(self.input_parameter)
 #   self.t+=[[model.predict(self.input_parameter),d,round(sht.read_t(),3),round(sht.read_rh(),3)]]
    self.ai=float(model.predict(self.input_parameter))


    #print(s,a,b,c,round(sht.read_t(),3),round(sht.read_rh(),3))

    # print (data[self.DUST_PM1_0_CF1], data[self.DUST_PM1_0_ATM])
    # print (data[self.DUST_PM2_5_CF1], data[self.DUST_PM2_5_ATM])
    # print (data[self.DUST_PM10_0_CF1], data[self.DUST_PM10_0_ATM])
    # print ("0.3um in 0.1L of air : %s" % (data[self.DUST_AIR_0_3]))
    # print ("0.5um in 0.1L of air : %s" % (data[self.DUST_AIR_0_5]))
    # print ("1.0um in 0.1L of air : %s" % (data[self.DUST_AIR_1_0]))
    # print ("2.5um in 0.1L of air : %s" % (data[self.DUST_AIR_2_5]))
    # print ("5.0um in 0.1L of air : %s" % (data[self.DUST_AIR_5_0]))
    # print ("10.0um in 0.1L of air : %s" % (data[self.DUST_AIR_10_0]))
    # print ("Reserved F : %s | Reserved B : %s" % (data[self.RESERVEDF],data[self.RESERVEDB]))
    # print ("CHKSUM : %s | read CHKSUM : %s | CHKSUM result : %s" % (chksum, data[self.CHECKSUM], chksum == data[self.CHECKSUM]))
    # print ("============================================================================")
    self.n+=1


    try:
      ser6.write(serial.to_bytes([0x02,0x52,0x00,0x00,0x03]))
      send1="0252000003"
#send1=int(send1,16)
#send1=send1.encode('utf-8')
    #byteToRead1 = ser6.inWaiting()
      s= ser6.readline()
      s=str(s)
      s=s.split(',')
      print(s)
#    gas=s[1]+","+s[2]+","+s[3]+","+s[4]+","+s[6]+","+s[7]+model.predict(self.input_parameter)+","+d+","+sht.read_t()+","+sht.read_rh()
#    print(gas)
      time_now=datetime.datetime.now()
      self.send=str("AI PM 2.5 :"+str(round(self.ai,2)))+", Raw PM 2.5 :"+str(round(d,2))+", Temp :"+str(round(sht.read_t(),2))+", Humidity :"+str(round(sht.read_rh(),2))+", CO :"+str(round(float(s[1])/1.2,2))+", SO2 :"+s[2]+", H2S :"+s[3]+", VOC: "+str(round(float(s[4])/3.5,2))+", NO2: "+s[6]+", O3: "+s[7]+"\r\n"
      self.send2=str(time_now)+" , "+str("AI PM 2.5 :"+str(round(self.ai,2)))+", Raw PM 2.5 :"+str(round(d,2))+", Temp :"+str(round(sht.read_t(),2))+", Humidity :"+str(round(sht.read_rh(),2))+", CO :"+str(round(float(s[1])/1.2,2))+", SO2 :"+s[2]+", H2S :"+s[3]+", VOC: "+str(round(float(s[4])/3.5,2))+", NO2: "+s[6]+", O3: "+s[7]
    #str(float(s[4])/0.01+float(s[7]))
      self.send=self.send.encode('utf-8')
      #time.sleep(10)
      ser.write(self.send)
      print(time_now)
#   ser.write(s)
    #ser.write(self.send)
      #print(self.send)
      #print(ser6.isOpen())	
      self.t+=[[str(self.send2)]]
      self.n+=1
      ser6.write(serial.to_bytes([0x02,0x53,0x00,0x00,0x03]))		
    except:
      print('connect error \n') 
    if self.n==2:
        print("it's start")
#    if self.n==5:
#        print(self.n)
#        df=pd.DataFrame(self.t)
#        path="/home/mems/Desktop/test/"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".csv"
#        df.to_csv(path)
#        print(self.n,"seconds _and save file")
    if self.n%100==0:
        #print(self.n)
        df=pd.DataFrame(self.t)
        path="/home/omni/Desktop/test2/"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".csv"
        df.to_csv(path)
        #print(self.n,"seconds _and save file")
        self.t=[]




# UART / USB Serial : 'dmesg | grep ttyUSB'
#USB0 = '/dev/ttyUSB0'
UART = '/dev/ttyAMA0'
#USB1 = '/dev/ttyUSB4'
#USB2 = '/dev/ttyUSB5'


ser6= serial.Serial(port='/dev/ttyUSB0',baudrate=57600,timeout=0)
ser6.write(serial.to_bytes([0x02,0x52,0x00,0x00,0x03]))

# USE PORT
SERIAL_PORT = UART 
#SERIAL_PORT1 = USB1
#SERIAL_PORT2 = USB2


# Baud Rate
Speed = 9600


# example
if __name__=='__main__':

  #serial setting
  #ser = serial.Serial(SERIAL_PORT, Speed, timeout = 1)
  #ser1 = serial.Serial(SERIAL_PORT1, Speed, timeout = 1)

  dust = PMS7003()
  #dust1 = PMS7003()
  #dust2 = PMS7003()
 # while True:
    #while True :
  ser=serial.Serial(SERIAL_PORT,Speed,timeout=0.5)
#  s1 = time.time()
      #time.sleep(1)
        #break
    #while 1 :
  #ser.flushInput()
  #ser1.flushInput()
  #ser2.flushInput()
        #time.sleep(1)
        #break
  buffer = ser.read(1024)
#  d=True
  #buffer1 = ser1.read(1024)
  #buffer2 = ser2.read(1024)
  while True:
    ser.flushInput()
    #ser1.flushInput()
    #ser2.flushInput()
    buffer =ser.read(1024)
    
    
    #buffer1 = ser1.read(1024)
    #buffer2 = ser2.read(1024)
#    if d:
    if(dust.protocol_chk(buffer)):
      dust.print_serial(buffer)
#      d=False

#    time_check = time.time() - s1
#    if time_check > 298 :
#      if(dust.protocol_chk(buffer)):
      
    if dust.data1 != None:
      k=1
      for l in dust.data1[3:]:
        m=Label(gasFrame, text="%.3f" %float(l),font = ('Times New Roman', 30,'bold'), width=25,height=1, relief=RIDGE)
        m.grid(row=k, column=1,sticky=NSEW,padx=5, pady=8)
        k+=1
      m=Label(leftFrame, text="%.1f " %float(dust.data1[0]),font = ('Times New Roman',30,'bold'), width=25,height=4, relief=RIDGE)
      m.grid(row=0, column=1,sticky=NSEW,padx=5, pady=15)
      m=Label(otherFrame, text="%.1f °C" %float(dust.data1[1]),font = ('Times New Roman', 23,'bold'),width=12,height=3, relief=RIDGE)
      m.grid(row=0, column=1,sticky=NSEW,padx=5, pady=10)
      m=Label(otherFrame, text="%.1f" %float(dust.data1[2]) + ' RH%',font = ('Times New Roman',23,'bold'), width=12,height=3, relief=RIDGE)
      m.grid(row=1, column=1,sticky=NSEW,padx=5, pady=10)

   
      tk.update()
      time.sleep(0.1) 

#        dust.print_serial(buffer)
#        s1 = time.time()
     # ser=serial.Serial(SERIAL_PORT,Speed,timeout=1)
      #ser.flushInput()

      #buffer = ser.read(1024)

    #if(dust1.protocol_chk(buffer1)):
      #print("DATA2 read success")

      # print data
      #dust1.print_serial(buffer1)
     # ser1=serial.Serial(SERIAL_PORT1,Speed,timeout=1)
      #ser1.flushInput()
     # buffer1 = ser.read(1024)


    #if(dust1.protocol_chk(buffer1)):
      #dust1.print_serial(buffer1)
    #if(dust2.protocol_chk(buffer2)):
      #print("DATA3 read ")
      #dust2.print_serial(buffer2)
      #ser2.flushInput()
#    else:
        #print("restart please")
#        continue


 # ser.close()
 # ser1.close()
