import time
import serial
from function_data import * # DECIMAL FROM FLOAT32 INT32 UNINT16 INT32-M10K
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

############################## OPEN SERIAL PORT ###############################

#ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3)

######################################## REQUEST ###################################################

###  SEM ONE METERING DEVICE ###
req1_1=b'\x40\x04\x00\x02\x00\x0C\x5E\xDE' #ser.read(29)  3+2*2*6+2

############################## DEFINE PAYLOADS ###############################

TOKEN = "BBFF-pCiZMmMBWqtLVjivm2tT8SFfDU2h70"  # Put your TOKEN here
DEVICE_1  = "drex_minigrid_1"  # Put your device label here

####### DEVICE VARIABLES  #######
i = v = wh =  0

####### REQUEST UBIDOTS FUNCTION #######
loop_c=0
wh_acum=0
t_port=0.5
t=10 #seconds

def get_log():
    try:
        ########################################  SEM ONE METERING DEVICE #########################################
        ############## ID: 64  ##################
        global wh_acum
        ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=3)
        time.sleep(t_port)
        print("SEM ONE")
        req = req1_1  # SEM ONE PARAMETERS
        #print("Writing ",str(req))
        ser.write(req)
        #ser.read(29)  3+2*2*6+2
        r=ser.read(29)
        #print("r:",r)
        if len(r) > 28:
            v = function2(r[3], r[4], r[5], r[6]) * (2 / 10)
            i = function2(r[7], r[8], r[9], r[10]) * (100 / 1000)
            if abs(v) > 300:
                v = 0
            if abs(i) > 300:
                i = 0

        wh = v * i * (t / (60 * 60))
        wh_acum = wh_acum + wh

        return {
            "success": True,
            "voltage": v,
            "current": i,
            "energy": wh,
            "energy-acum": wh_acum
        }

    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        print("connection error")
