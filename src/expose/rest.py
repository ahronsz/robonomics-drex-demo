import requests
import json
import logging
import csv_functions as csv
from global_variables import *

def save_energy_data(energy_data):
    _url = f"{BASE_URL_BACKEND_CONSUME}/record"
    try:
        response = requests.post(
            url = _url, 
            data = json.dumps(energy_data), 
            headers = {'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        logging.info(f"Data grid sent: {energy_data}")
    except requests.exceptions.HTTPError as e:
        logging.error("Api Exception: {}".format(e))
        csv.append_data_grid(BACKUP_FILE_ENERGY_DATA, energy_data)
    except requests.exceptions.RequestException as e:
        logging.error("Failed to establish connection to the backend")