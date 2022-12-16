import logging
import os
import csv
from csv import DictWriter
from global_variables import *

headers_energy_data = ['device-code', 'energy-accumulated', 'timestamp']

def append_data_grid(type_backup, energy_data):
    headers = headers_energy_data
    path = f"{BACKUP_FILES_DIR}/{type_backup}"

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


def delete_file_csv(type_backup):
    path = f"{BACKUP_FILES_DIR}/{type_backup}"
    if(isExistsFile(path)):
        try:
            os.remove(path)
        except Exception as e:
            logging.error(f"Failed to delete csv file backup: {e}")

def isExistsFile(path):
    return os.path.exists(path) and os.path.isfile(path)





