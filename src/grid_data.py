import logging
import os
import errno
import csv
from csv import DictWriter
import os.path
from global_variables import *

#headers_energy_data = ['grid-id', 'voltage', 'current', 'energy', 'energy-acum', 'datetime']
#headers_last_trigger = ['start', 'end', 'datetime']

def append_data_grid(type_backup, energy_data):
    path = f"{BACKUP_FILES_DIR}/{type_backup}"
    headers = HEADERS_ENERGY_DATA if type_backup != BACKUP_FILE_ROBONOMICS else HEADERS_LAST_TRIGGER
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
        logging.error(f"Failed to create csv file backup: {e}")

def get_last_trigger_meter():
    path = f"{BACKUP_FILES_DIR}/{LAST_RECORD_TRIGGER}"
    data = {}
    try:
        if(isExistsFile(path)):
            with open(path) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for rows in csv_reader:
                    data = rows
            return data["end"]
        else:
            return 0
    except Exception:
        return 0

def save_last_trigger_meter(energy_data):
    path = f"{BACKUP_FILES_DIR}/{LAST_RECORD_TRIGGER}"
    delete_file_csv(path)
    append_data_grid(energy_data)

def delete_file_csv(type_backup):
    path = BACKUP_FILES_DIR + type_backup
    if(isExistsFile(path)):
        try:
            os.remove(path)
        except Exception as e:
            logging.error(f"Failed to delete csv file backup: {e}")

def isExistsFile(path):
    return os.path.exists(path) and os.path.isfile(path)





