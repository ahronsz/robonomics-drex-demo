import logging
import os
import csv
from csv import DictWriter
from os.path import exists as file_exists
from global_variables import *

headers_energy_data = ['grid-location', 'voltage', 'current', 'energy', 'energy-accumulated', 'timestamp']
headers_last_trigger = ['last-meter', 'energy-remainder', 'timestamp']

def append_data_grid(type_backup, energy_data):
    headers = ""
    path = f"{BACKUP_FILES_DIR}/{type_backup}"
    
    if type_backup == LAST_RECORD_TRIGGER:
        headers = headers_last_trigger
    if type_backup == BACKUP_FILE_ENERGY_DATA:
        headers = headers_energy_data
    if type_backup == BACKUP_FILE_ROBONOMICS:
        headers = headers_energy_data

    #headers = headers_energy_data if type_backup != LAST_RECORD_TRIGGER else headers_last_trigger
    if not (isExistsFile(path)):
        create_file_csv(path, headers)    
    try:
        with open(path, 'a') as f_object:
            dict_writer_object = DictWriter(f_object, fieldnames = headers)
            dict_writer_object.writerow(energy_data)
            f_object.close()
        logging.info(f"Data grid successfully sent to csv backup file: {type_backup}")
    except Exception as e:
        logging.error(f"Failed to edit csv file backup: {e}")

def create_file_csv(path, headers):
    try:
        # Create target Directory
        with open(path, "w") as f_object:
            grid = csv.writer(f_object)
            grid.writerow(headers)
            f_object.close()
            logging.info(f"Backup CSV file created successfully")
    except Exception as e:
        logging.debug(f"Failed to create csv file backup: {e}")

def save_last_trigger_meter(energy_data, energy_remainder: str):
    last_trigger_meter = {
        "last-meter": energy_data["energy-accumulated"],
        "energy-remainder": energy_remainder,
        #"energy-remainder": energy_data["energy-accumulated"] - get_last_trigger_meter("last-meter"),
        "timestamp": energy_data["timestamp"]
    }
    path = f"{BACKUP_FILES_DIR}/{LAST_RECORD_TRIGGER}"
    delete_file_csv(path)
    append_data_grid(LAST_RECORD_TRIGGER, last_trigger_meter)

def get_last_trigger_meter(attribute: str = None):
    path = f"{BACKUP_FILES_DIR}/{LAST_RECORD_TRIGGER}"
    data = {}
    try:
        if (isExistsFile(path)):
            with open(path) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for rows in csv_reader:
                    data = rows
            return data[attribute] if attribute else data
        else:
            data = {
                "last-meter": 0,
                "energy-remainder": 0,
                "timestamp": currentTimestamp()
            }
            return data[attribute] if attribute else data
    except Exception as e:
        logging.error(f"Failed to get csv file backup: {e}")

def csvToArrayJson():
    try:
        data = []
        with open(f"{BACKUP_FILES_DIR}/{BACKUP_FILE_ROBONOMICS}") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for rows in csv_reader:
                data.append(rows)
        return data
    except Exception as e:
        logging.error(f"Failed to get csv file backup: {e}")


def delete_file_csv(type_backup):
    path = f"{BACKUP_FILES_DIR}/{type_backup}"
    if(isExistsFile(path)):
        try:
            os.remove(path)
        except Exception as e:
            logging.error(f"Failed to delete csv file backup: {e}")

def isExistsFile(path):
    return os.path.exists(path) and os.path.isfile(path)





