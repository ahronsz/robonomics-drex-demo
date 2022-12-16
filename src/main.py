#!/usr/bin/env python3
import time
import serial
import logging
import requests
#import pandas as pd
from function_data import * # DECIMAL FROM FLOAT32 INT32 UNINT16 INT32-M10K
import csv_functions
import expose.rest as rest
from global_variables import *
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

############################## OPEN SERIAL PORT ###############################

#ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3)

######################################## REQUEST ###################################################

###  Voltage and Amper###
req1_1=b'\x01\x04\x00\x02\x00\x04\x50\x09' #ser.read(13)  3+2*2*2+2 SO1
req2_1=b'\x02\x04\x00\x02\x00\x04\x50\x3A' #ser.read(13)  3+2*2*2+2 SO2
req3_1=b'\x03\x04\x00\x02\x00\x04\x51\xEB' #ser.read(13)  3+2*2*2+2 SO3

###  Energies ###
req1_2=b'\x01\x04\x00\x3C\x00\x02\xB1\xC7' #ser.read(9)   3+1*2*2+2 SO1
req2_2=b'\x02\x04\x00\x3C\x00\x02\xB1\xF4' #ser.read(9)   3+1*2*2+2 SO2
req3_2=b'\x03\x04\x00\x3C\x00\x02\xB0\x25' #ser.read(9)   3+1*2*2+2 SO3

############################## DEFINE PAYLOADS ###############################

TOKEN     = "BBFF-pCiZMmMBWqtLVjivm2tT8SFfDU2h70"  # Put your TOKEN here
DEVICE_1  = DEVICE_CODE  # Put your device label here

####### DEVICE LABELS  #######
LABEL_1 = "energy_cum_1" # Put your first variable label here
LABEL_2 = "energy_cum_2" # Put your first variable label here
LABEL_3 = "energy_cum_3" # Put your first variable label here
LABEL_4 = "energy_cum_total" # Put your first variable label here
LABEL_5 = "power"
####### DEVICE VARIABLES  #######
i1   = i2   = i3   = 0
v1   = v2   = v3   = 0
kwh1 = kwh2 = kwh3 = 0
kwh_acum = 0
kw=0

####### PAYLOAD FUNCTION #######
def build_payload(labels, *args):
    payload = {}
    for label, value in zip(labels, args):
        payload[label] = value
    return payload

####### REQUEST UBIDOTS FUNCTION #######
####### REQUEST UBIDOTS FUNCTION #######
def post_request(device,payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url,device)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        try:
            req = requests.post(url=url, headers=headers, json=payload)##############################
            status = req.status_code
            attempts += 1
            time.sleep(1)
        except:
            print("Upload error")
            #pass
    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

loop_c=0
loop_t=0
t=5 #seconds
#wh_acum=0
t_port=0.5


while True:
    try:

        ########################################  SO 1 : voltage and amper #########################################
        ############## ID: 01  ##################
        ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3)
        time.sleep(t_port)
        print("Sem One 1:")
        req = req1_1 #print("Writing ",str(req))
        ser.write(req)
        r=ser.read(13) #ser.read(13)  3+2*2*2+2
        if len(r)>12:
            v1   =(function2(r[3],r[4],r[5],r[6]))/10
            i1   =(function2(r[7],r[8],r[9],r[10]))*(2.5/1000)
        print("SO1 voltage:", v1)
        print("SO1 corriente:", i1)
        time.sleep(t)

        ########################################  SO 2 : voltage and amper #########################################
        ############## ID: 02  ##################
        ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3)
        time.sleep(t_port)
        print("Sem One 2:")
        req = req2_1 #print("Writing ",str(req))
        ser.write(req)
        r=ser.read(13) #ser.read(13)  3+2*2*2+2
        if len(r)>12:
            v2   =(function2(r[3],r[4],r[5],r[6]))/10
            i2   =(function2(r[7],r[8],r[9],r[10]))*(2.5/1000)
        print("SO2 voltage:", v2)
        print("SO2 corriente:", i2)
        time.sleep(t)

        ########################################  SO 3 : voltage and amper #########################################
        ############## ID: 03  ##################
        ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3)
        time.sleep(t_port)
        print("Sem One 3:")
        req = req3_1 #print("Writing ",str(req))
        ser.write(req)
        r=ser.read(13) #ser.read(13)  3+2*2*2+2
        if len(r)>12:
            v3   =(function2(r[3],r[4],r[5],r[6]))/10
            i3   =(function2(r[7],r[8],r[9],r[10]))*(2.5/1000)
        print("SO3 voltage:", v3)
        print("SO3 corriente:", i3)
        time.sleep(t)

        ########################################  SO 1 : energy #########################################
        ############## ID: 01  ##################
        ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3)
        time.sleep(t_port)
        print("Sem One 1:")
        req = req1_2 #print("Writing ",str(req))
        ser.write(req)
        r=ser.read(9) #ser.read(9)  3+1*2*2+2
        if len(r)>8:
            kwh1 =(function2(r[3],r[4],r[5],r[6]))*(2.5/1000)
        print("SO1 energia:", kwh1)
        time.sleep(t)

        ########################################  SO 2 : energy #########################################
        ############## ID: 02  ##################
        ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3)
        time.sleep(t_port)
        print("Sem One 2:")
        req = req2_2 #print("Writing ",str(req))
        ser.write(req)
        r=ser.read(9) #ser.read(9)  3+1*2*2+2
        if len(r)>8:
            kwh2 =(function2(r[3],r[4],r[5],r[6]))*(2.5/1000)
        print("SO2 energia:", kwh2)
        time.sleep(t)

        ########################################  SO 3 : energy #########################################
        ############## ID: 03  ##################
        ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3)
        time.sleep(t_port)
        print("Sem One 3:")
        req = req3_2 #print("Writing ",str(req))
        ser.write(req)
        r=ser.read(9) #ser.read(9)  3+1*2*2+2
        if len(r)>8:
            kwh3 =(function2(r[3],r[4],r[5],r[6]))*(2.5/1000)
        print("SO3 energia:", kwh3)
        time.sleep(t)


        ######## TOTALIZER KWH ACUM ######
        kwh_acum = (kwh1 + kwh2 + kwh3)*3
        kw = ((v1*i1 + v2*i2 + v3*i3)*3)/1000
        print("energy total:", kwh_acum)

        #ser.close()
        loop_c=loop_c+1
        loop_t=loop_t+1
        print("Loop Counter",loop_c)
        print("")
        time.sleep(t)
        time.sleep(t*6)

        if loop_c>=1: ##loop 1 is equal to 1 minute
            loop_c=0
            ser.close()
            time.sleep(t_port)

            ########## SENDING DATA TO UBIDOTS ##########
            print("Making payload 1")
            labels = [LABEL_1, LABEL_2, LABEL_3,LABEL_4,LABEL_5]
            payload = build_payload( labels, kwh1, kwh2, kwh3, kwh_acum,kw)
            print("Payload  is -->",payload)
            print("[INFO] Attemping to send data")
            post_request(DEVICE_1,payload)
            time.sleep(1)

        if loop_t>=EACH_MINUTE: ##loop 1 is equal to 1 minute
            loop_t=0
            ########## SENDING DATA TO ROBONOMICS ##########
            print(kwh_acum)
            data = {
                "device-code": DEVICE_1,
                "energy-accumulated": kwh_acum,
                "timestamp": currentTimestamp()
            }
            if(csv_functions.isExistsFile(f"{BACKUP_FILES_DIR}/{BACKUP_FILE_ENERGY_DATA}")):
                rest.send_batch_energy_data()
            rest.save_energy_data(data) #Save energy data to backend

    

    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        print("connection error")
        time.sleep(5)