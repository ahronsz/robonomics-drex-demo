import os
import time
import datetime
import json
import serial
import requests
import sys, select
import struct
import random
import math
import csv_functions
import logging
import expose.rest as rest
from global_variables import *
#import pandas as pd
from function_data import * # DECIMAL FROM FLOAT32 INT32 UNINT16 INT32-M10K
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)
############################## OPEN SERIAL PORT ###############################

#ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=3)

######################################## REQUEST ###################################################

###  SEM ONE METERING DEVICE ###
req1_1=b'\x40\x04\x00\x02\x00\x0C\x5E\xDE' #ser.read(29)  3+2*2*6+2

############################## DEFINE PAYLOADS ###############################

TOKEN = "BBFF-pCiZMmMBWqtLVjivm2tT8SFfDU2h70"  # Put your TOKEN here
DEVICE_1  = DEVICE_CODE  # Put your device label here

####### DEVICE LABELS  #######
LABEL_1 = "energy" # Put your first variable label here


####### DEVICE VARIABLES  #######
i = v = wh =  wh_acum =0

####### PAYLOAD FUNCTION #######
def build_payload(labels, *args):
    payload = {}
    for label, value in zip(labels, args):
        payload[label] = value
    return payload

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
t_port=0.5
t=10 #seconds
grid_id=1

while True:

    try:

        ########################################  SEM ONE METERING DEVICE #########################################
        ############## ID: 64  ##################

        ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=3)
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
        ######## TOTALIZER KWH ACUM ######
        wh_acum = wh_acum + wh
        print("energy total:", wh_acum)


        #ser.close()
        loop_c=loop_c+1
        print("Loop Counter",loop_c)
        print("")
        time.sleep(t*6) ## t=10s, sleep = 60s = 1minute

        if loop_c>=1: ##loop 1 is equal to 1 minute
            loop_c=0
            ser.close()
                    #time.sleep(t_port)

            ########## SENDING DATA TO UBIDOTS ##########
            print("Making payload 1")
            labels = [LABEL_1]
            payload = build_payload( labels, wh_acum)
            print("Payload  is -->",payload)
            print("[INFO] Attemping to send data")
            post_request(DEVICE_1,payload)
            time.sleep(1)

        if loop_t>=EACH_MINUTE: ##loop 5 is equal to 5 minute
            loop_t=0
            ########## SENDING DATA TO BACKEND ##########
            data = {
                "device-code": DEVICE_1,
                "energy-accumulated": wh_acum,
                "timestamp": currentTimestamp()
            }
            threads = list()
            if(csv_functions.isExistsFile(f"{BACKUP_FILES_DIR}/{BACKUP_FILE_ENERGY_DATA}")):
                rest.send_batch_energy_data()
            #Save energy data to backend    
            rest.save_energy_data(data)
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        print("connection error")