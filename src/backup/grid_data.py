import logging
import os
import errno
import csv
from csv import DictWriter
import os.path
from global_variables import *

headers = ['grid-code', 'voltage', 'current', 'energy', 'energy-acum', 'timestamp']

def append_data_grid(type, data):
    path = BACKUP_FILES_DIR + type
    if(os.path.exists(path)):
        try:
            with open(path, 'a') as f_object:
                dict_writer_object = DictWriter(f_object, fieldnames = headers)
                dict_writer_object.writerow(data)
                f_object.close()
            logging.info(f"Data grid successfully sent to csv backup file: {type}")
        except Exception as e:
            logging.error(f"Failed to edit csv file backup: {e}")    
    else:
        create_file_csv(path)

def create_file_csv(path):
    try:
        # Create target Directory
        with open(path, "w") as f_object:
            grid = csv.writer(f_object)
            grid.writerow(headers)
            f_object.close()
            logging.info(f"Backup CSV file created successfully: {type}")
    except Exception as e:
        logging.error(f"Failed to create csv file backup: {e}")

def delete_file_csv(path):
    path = BACKUP_FILES_DIR + type
    if(os.path.exists(path) and os.path.isfile(path)):
        try:
            os.remove(path)
        except Exception as e:
            logging.error(f"Failed to delete csv file backup: {e}")



