import time
import logging
#import serial
from function_data import * # DECIMAL FROM FLOAT32 INT32 UNINT16 INT32-M10K
from global_variables import currentTimestamp

############################## OPEN SERIAL PORT ###############################

#ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3)

######################################## REQUEST ###################################################

###  SEM ONE METERING DEVICE ###
req1_1=b'\x40\x04\x00\x02\x00\x0C\x5E\xDE' #ser.read(29)  3+2*2*6+2

############################## DEFINE PAYLOADS ###############################

#TOKEN = "BBFF-pCiZMmMBWqtLVjivm2tT8SFfDU2h70"  # Put your TOKEN here
#DEVICE_1  = "drex_minigrid_1"  # Put your device label here

####### DEVICE VARIABLES  #######
i = v = wh =  0

####### REQUEST UBI_DOTS FUNCTION #######
loop_c=0
wh_accumulated=0
t_port=0.5
t=60 #seconds
grid_id=1

def get_energy_data():
    try:
        
        ########################################  SEM ONE METERING DEVICE #########################################
        ############## ID: 64  ##################
        global wh_accumulated
        ser = serial.Serial('/dev/ttyAMA0', baudrate = 9600, timeout = 3)
        time.sleep(t_port)
        print("SEM ONE")
        req = req1_1  # SEM ONE PARAMETERS
        #print("Writing ",str(req))
        ser.write(req)
        #ser.read(29)  3+2*2*6+2
        r = ser.read(29)
        #print("r:",r)
        if len(r) > 28:
            v = function2(r[3], r[4], r[5], r[6]) * (2 / 10)
            i = function2(r[7], r[8], r[9], r[10]) * (100 / 1000)
            if abs(v) > 300:
                v = 0
            if abs(i) > 300:
                i = 0

        wh = v * i * (t / (60 * 60))
        wh_accumulated = wh_accumulated + wh

        return {
            "grid-location": grid_id,
            "voltage": v,
            "current": i,
            "energy": wh,
            "energy-accumulated": wh_accumulated,
            "timestamp": currentTimestamp()
        }
        
        '''
        return {
            "grid-location": 0,
            "voltage": 238.60000000000002,
            "current": 0.0,
            "energy": 2.0516666666666667,
            "energy-accumulated": 50,
            "timestamp": currentTimestamp()
        }
        '''
    except Exception as e:
        logging.fatal(f"Failed to read grid data: {e}")
