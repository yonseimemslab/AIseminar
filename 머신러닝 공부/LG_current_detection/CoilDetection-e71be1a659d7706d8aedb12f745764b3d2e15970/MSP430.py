#############################################################################################

# Author: Jun Gong

# Function: MSP430 Initializer

# Note: Please change the configuration settings when switch to different coils

# Date: 05/07/2018

# /python -m serial.tools.list_ports

#############################################################################################

import serial

import time

import binascii

import serial.tools.list_ports

import os



os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import threading



#############################################################################################

# LDC1614 addressing space

LDC1614_DATA_MSB_CH0 = '00'

LDC1614_DATA_LSB_CH0 = '01'

LDC1614_DATA_MSB_CH1 = '02'

LDC1614_DATA_LSB_CH1 = '03'

LDC1614_DATA_MSB_CH2 = '04'

LDC1614_DATA_LSB_CH2 = '05'

LDC1614_DATA_MSB_CH3 = '06'

LDC1614_DATA_LSB_CH3 = '07'

LDC1614_RCOUNT_CH0 = '08'

LDC1614_RCOUNT_CH1 = '09'

LDC1614_RCOUNT_CH2 = '0A'

LDC1614_RCOUNT_CH3 = '0B'

LDC1614_OFFSET_CH0 = '0C'

LDC1614_OFFSET_CH1 = '0D'

LDC1614_OFFSET_CH2 = '0E'

LDC1614_OFFSET_CH3 = '0F'

LDC1614_SETTLECOUNT_CH0 = '10'

LDC1614_SETTLECOUNT_CH1 = '11'

LDC1614_SETTLECOUNT_CH2 = '12'

LDC1614_SETTLECOUNT_CH3 = '13'

# CHx_FREF_DIVIDER [9:0] && CHx_FIN_DIVIDER [15:12]

LDC1614_CLOCK_DIVIDERS_CH0 = '14'

LDC1614_CLOCK_DIVIDERS_CH1 = '15'

LDC1614_CLOCK_DIVIDERS_CH2 = '16'

LDC1614_CLOCK_DIVIDERS_CH3 = '17'

LDC1614_STATUS = '18'

LDC1614_ERROR_CONFIG = '19'

LDC1614_CONFIG = '1A'

LDC1614_MUX_CONFIG = '1B'

LDC1614_RESET_DEV = '1C'

LDC1614_DRIVE_CURRENT_CH0 = '1E'

LDC1614_DRIVE_CURRENT_CH1 = '1F'

LDC1614_DRIVE_CURRENT_CH2 = '20'

LDC1614_DRIVE_CURRENT_CH3 = '21'

LDC1614_MANUFACTURER_ID = '7E'

LDC1614_DEVICE_ID = '7F'



DEBUG_PRINT_TX_DATA = 0

DEBUG_PRINT_RX_DATA = 0

DEBUG_PRINT_READ_DATA = 0





class MSPComm:

    """

    read data from MSP430 and store in data_ch and base_ch

    """



    def __init__(self, port_name, msp_name):

        self.name = msp_name



        self.sampleSize = 100

        self.sample_time = 0.001  # second

        self.serial_port = serial.Serial(port=port_name, baudrate=115200)

        self.recorder = threading.Thread(target=self.record_data, name="recorder")



        # self.sender = threading.Thread(target = self.client, name = "sender")



        self.peak = 800000

        self.data_ch = [0] * 4

        self.base_ch = [0] * 4

        self.count = [0] * 4
        self.reset_baseline=0


        self.config()

        self.start()

        print ('build sucessful')



    class crc8:

        def __init__(self):

            self.crcTable = (0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 0x38,

                             0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d, 0x70, 0x77,

                             0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 0x48, 0x4f, 0x46,

                             0x41, 0x54, 0x53, 0x5a, 0x5d, 0xe0, 0xe7, 0xee, 0xe9,

                             0xfc, 0xfb, 0xf2, 0xf5, 0xd8, 0xdf, 0xd6, 0xd1, 0xc4,

                             0xc3, 0xca, 0xcd, 0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b,

                             0x82, 0x85, 0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba,

                             0xbd, 0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2,

                             0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea, 0xb7,

                             0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2, 0x8f, 0x88,

                             0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a, 0x27, 0x20, 0x29,

                             0x2e, 0x3b, 0x3c, 0x35, 0x32, 0x1f, 0x18, 0x11, 0x16,

                             0x03, 0x04, 0x0d, 0x0a, 0x57, 0x50, 0x59, 0x5e, 0x4b,

                             0x4c, 0x45, 0x42, 0x6f, 0x68, 0x61, 0x66, 0x73, 0x74,

                             0x7d, 0x7a, 0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b,

                             0x9c, 0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,

                             0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 0xc1,

                             0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4, 0x69, 0x6e,

                             0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c, 0x51, 0x56, 0x5f,

                             0x58, 0x4d, 0x4a, 0x43, 0x44, 0x19, 0x1e, 0x17, 0x10,

                             0x05, 0x02, 0x0b, 0x0c, 0x21, 0x26, 0x2f, 0x28, 0x3d,

                             0x3a, 0x33, 0x34, 0x4e, 0x49, 0x40, 0x47, 0x52, 0x55,

                             0x5c, 0x5b, 0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64,

                             0x63, 0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b,

                             0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13, 0xae,

                             0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 0x96, 0x91,

                             0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83, 0xde, 0xd9, 0xd0,

                             0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 0xe6, 0xe1, 0xe8, 0xef,

                             0xfa, 0xfd, 0xf4, 0xf3)



        def crc(self, msg):

            runningCRC = 0

            for c in msg:

                c = ord(str(c))

                runningCRC = self.crcByte(runningCRC, c)

            return runningCRC



        def crcByte(self, oldCrc, byte):

            res = self.crcTable[oldCrc & 0xFF ^ byte & 0xFF]

            return res



    def write_reg(self, addr, data):

        crc = self.crc8()

        serial_string = '4C150100042A' + addr + data

        serial_string=bytes.fromhex('4C150100042A').decode('utf-8')
        #serial_string = serial_string.decode('hex')

        crc_byte = chr(crc.crc(serial_string))

        self.serial_port.write(serial_string + crc_byte)

        s = self.serial_port.read(32)

        if DEBUG_PRINT_RX_DATA:

            print("Read:%s" % (binascii.hexlify(s)))

        if (s[3] != '\x00'):

            print("Error in write register")

            exit()



    def read_reg(self, addr):

        crc = self.crc8()

        serial_string = '4C150100022A' + addr

        serial_string=serial_string.decode('hex')
        #serial_string = serial_string.decode('hex')

        crc_byte = chr(crc.crc(serial_string))

        self.serial_port.write(serial_string + crc_byte)

        s = self.serial_port.read(32)

        if DEBUG_PRINT_RX_DATA:

            print("Read:%s" % (binascii.hexlify(s)))

        if (s[3] != '\x00'):

            print("Error in set register")

            exit()

        serial_string = '4C140100022A02'

        serial_string = serial_string.decode('hex')

        crc_byte = chr(crc.crc(serial_string))

        self.serial_port.write(serial_string + crc_byte)

        s = self.serial_port.read(32)

        if DEBUG_PRINT_RX_DATA:

            print("Read:%s" % (binascii.hexlify(s)))

        if (s[3] != '\x00'):

            print("Error in read register")

            exit()

        data_read = s[6] + s[7]

        if DEBUG_PRINT_READ_DATA:

            print("Addr:", addr, "Data:", binascii.hexlify(data_read))

        return binascii.hexlify(data_read)



    def ldc_start_streaming(self):

        # start streaming

        serial_stream_string = '4C0501000601290404302AC1'

        serial_stream_string = serial_stream_string.decode('hex')

        crc = self.crc8()

        crc_byte = chr(crc.crc(serial_stream_string))

        self.serial_port.write(serial_stream_string + crc_byte)

        s = self.serial_port.read(32)

        if DEBUG_PRINT_RX_DATA:

            print("Read:%s" % (binascii.hexlify(s)))

        if (s[3] != '\x00'):

            print("Error in write register")

            exit()



    def ldc_stop_streaming(self):

        # stop streaming

        serial_stop_stream_string = '4C0601000101D2'

        serial_stop_stream_string = serial_stop_stream_string.decode('hex')

        # serial_stop_stream_string = codecs.decode(serial_stop_stream_string, 'hex')



        crc = self.crc8()

        crc_byte = chr(crc.crc(serial_stop_stream_string))

        self.serial_port.write(serial_stop_stream_string + crc_byte)

        s = self.serial_port.read(32)

        if DEBUG_PRINT_RX_DATA:

            print("Read:%s" % (binascii.hexlify(s)))

        if (s[3] != '\x00'):

            print("Error in write register")

            exit()



    def config(self):

        device_id = self.read_reg(LDC1614_DEVICE_ID)

        print("device_id=" + self.name)

        #################Configuration Settings#################



        self.write_reg(LDC1614_RCOUNT_CH0, "2d6b")

        self.write_reg(LDC1614_RCOUNT_CH1, "2d6b")

        self.write_reg(LDC1614_RCOUNT_CH2, "2d6b")

        self.write_reg(LDC1614_RCOUNT_CH3, "2d6b")

        self.write_reg(LDC1614_SETTLECOUNT_CH0, "0007")

        self.write_reg(LDC1614_SETTLECOUNT_CH1, "0007")

        self.write_reg(LDC1614_SETTLECOUNT_CH2, "0007")

        self.write_reg(LDC1614_SETTLECOUNT_CH3, "0007")

        self.write_reg(LDC1614_CLOCK_DIVIDERS_CH0, "1002")

        self.write_reg(LDC1614_CLOCK_DIVIDERS_CH1, "1002")

        self.write_reg(LDC1614_CLOCK_DIVIDERS_CH2, "1002")

        self.write_reg(LDC1614_CLOCK_DIVIDERS_CH3, "1002")

        self.write_reg(LDC1614_ERROR_CONFIG, "0000")

        self.write_reg(LDC1614_MUX_CONFIG, "C20D")

        self.write_reg(LDC1614_DRIVE_CURRENT_CH0, "9000")

        self.write_reg(LDC1614_DRIVE_CURRENT_CH1, "9000")

        self.write_reg(LDC1614_DRIVE_CURRENT_CH2, "9000")

        self.write_reg(LDC1614_DRIVE_CURRENT_CH3, "9000")

        self.write_reg(LDC1614_CONFIG, "1601")



        ########################################################


        for i in range(5):
            data_msb = self.read_reg(LDC1614_DATA_MSB_CH0)

            data_lsb = self.read_reg(LDC1614_DATA_LSB_CH0)

            data_msb = self.read_reg(LDC1614_DATA_MSB_CH1)

            data_lsb = self.read_reg(LDC1614_DATA_LSB_CH1)

            data_msb = self.read_reg(LDC1614_DATA_MSB_CH2)

            data_lsb = self.read_reg(LDC1614_DATA_LSB_CH2)

            data_msb = self.read_reg(LDC1614_DATA_MSB_CH3)

            data_lsb = self.read_reg(LDC1614_DATA_LSB_CH3)



        time.sleep(1)


        data_msb = self.read_reg(LDC1614_DATA_MSB_CH0)

        data_lsb = self.read_reg(LDC1614_DATA_LSB_CH0)

        self.data_ch[0] = int(data_msb, 16) * 65536 + int(data_lsb, 16)


        data_msb = self.read_reg(LDC1614_DATA_MSB_CH1)

        data_lsb = self.read_reg(LDC1614_DATA_LSB_CH1)

        self.data_ch[1] = int(data_msb, 16) * 65536 + int(data_lsb, 16)

        data_msb = self.read_reg(LDC1614_DATA_MSB_CH2)

        data_lsb = self.read_reg(LDC1614_DATA_LSB_CH2)

        self.data_ch[2] = int(data_msb, 16) * 65536 + int(data_lsb, 16)

        data_msb = self.read_reg(LDC1614_DATA_MSB_CH3)

        data_lsb = self.read_reg(LDC1614_DATA_LSB_CH3)

        self.data_ch[3] = int(data_msb, 16) * 65536 + int(data_lsb, 16)


        for i in range(4):

            self.base_ch[i] = self.data_ch[i]



        print('Data: ' + str(self.data_ch))

        print('Base: ' + str(self.base_ch))



    def record_data(self):

        try:

            while 1:

                data_lsb = self.read_reg(LDC1614_DATA_LSB_CH0)

                data_msb = self.read_reg(LDC1614_DATA_MSB_CH0)

                self.data_ch[0] = int(data_msb, 16) * 65536 + int(data_lsb, 16)

                data_lsb = self.read_reg(LDC1614_DATA_LSB_CH1)

                data_msb = self.read_reg(LDC1614_DATA_MSB_CH1)

                self.data_ch[1] = int(data_msb, 16) * 65536 + int(data_lsb, 16)

                data_lsb = self.read_reg(LDC1614_DATA_LSB_CH2)

                data_msb = self.read_reg(LDC1614_DATA_MSB_CH2)

                self.data_ch[2] = int(data_msb, 16) * 65536 + int(data_lsb, 16)

                data_lsb = self.read_reg(LDC1614_DATA_LSB_CH3)

                data_msb = self.read_reg(LDC1614_DATA_MSB_CH3)

                self.data_ch[3] = int(data_msb, 16) * 65536 + int(data_lsb, 16)

                # print (str(self.data_ch[0])+' '+str(self.data_ch[1])+' '+str(self.data_ch[2])+' '+str(self.data_ch[3]))

                self.update_baseline()

                if self.reset_baseline==1:

                    for i in range(4):
                        self.base_ch[i] = self.data_ch[i]
                        print(self.base_ch[i])
                    self.reset_baseline=0

                time.sleep(self.sample_time)

        except KeyboardInterrupt:

            exit()


    def reset_base(self):
        self.reset_baseline=1

    def update_baseline(self):

        for i in range(4):

            if self.data_ch[i] > self.base_ch[i]:

                self.base_ch[i] += int(self.peak * 1.0 / 16000000)

            else:

                self.base_ch[i] -= int(self.peak * 1.0 / 16000000)



    def client(self):

        try:

            while 1:

                line = self.name + " "

                for i in range(4):

                    line += str(self.data_ch[i]) + " "

                line.strip()

                self.s.send(line + "\n")



                time.sleep(self.send_time)

        except KeyboardInterrupt:

            self.s.close()

            exit()



    def start(self):

        self.recorder.start()

        # self.sender.start()

