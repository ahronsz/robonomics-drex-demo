import requests
import json
import logging
import csv_functions as csv
from global_variables import *

_url = f"{BASE_URL_BACKEND_CONSUME}/grid"

def save_energy_data(energy_data):
    try:
        response = requests.post(
            url = _url, 
            data = json.dumps(energy_data), 
            headers = {'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        logging.info(f"Data grid sent: {energy_data}")
    except requests.exceptions.HTTPError as e:
        csv.append_data_grid(BACKUP_FILE_ENERGY_DATA, energy_data)
        logging.error("Api Exception: {}".format(e))
    except requests.exceptions.RequestException as e:
        csv.append_data_grid(BACKUP_FILE_ENERGY_DATA, energy_data)
        logging.error("Failed to establish connection to the backend")


def send_batch_energy_data():
    try:
        _files = {
            "file": (
                "batch_energy_data.csv",
                open(f"{BACKUP_FILES_DIR}/{BACKUP_FILE_ENERGY_DATA}", "rb"),
                "text/csv",
                {"Expires": "0"}
            )
        }
        response = requests.post(
            url = f"{_url}/batch", 
            files = _files
        )
        response.raise_for_status()
        csv.delete_file_csv(BACKUP_FILE_ENERGY_DATA)
        logging.info(f"Data csv grid sent: {BACKUP_FILE_ENERGY_DATA}")
    except requests.exceptions.HTTPError as e:
        logging.error("Api Exception: {}".format(e))
    except requests.exceptions.RequestException as e:
        logging.error("Failed to establish connection to the backend")