'''
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████╗░░██████╗░░███████╗░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██╔══██╗░██╔══██╗░██╔════╝░█╗░░░█╗░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║░░██║░██████╔╝░█████╗░░░░█║░█╔╝░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██║░░██║░██╔══██╗░██╔══╝░░░░░██═╝░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████╔╝░██║░░██║░███████╗░░█╔═█╗░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█████╔╝░░██║░░██║░███████║░█╔╝░░█╗░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
'''
import logging
import time
import json
import sys
import expose.rest as rest
import rpi_functions as rpi
import csv_functions
import threading
from global_variables import *

from robonomicsinterface import Account, Datalog

sys.dont_write_bytecode = True
# set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

try:
    account_with_seed = Account(seed = SEED, remote_ws = RPC_ROBONOMICS)
    data_log = Datalog(account_with_seed)
except Exception as e:
    logging.error(e)
    raise SystemExit

# Start solar panel daemon
logging.info("Started main Solar panel daemon.")

while True:
    energy_data = rpi.get_energy_data()
    last_trigger_meter = csv_functions.get_last_trigger_meter() #Obtiene el ultimo registro que logro alcanzar el acumulado de 1000 KWt

    #Si el acumulado es mayor que el ultimo registro alcanzado, se reinicia el contador.
    if(energy_data["energy-accumulated"] >= int(last_trigger_meter["last-meter"])):
        energy_accumulated = energy_data["energy-accumulated"] + int(last_trigger_meter["energy-remainder"])
        amount_trigger = int(last_trigger_meter["last-meter"]) + KW_H
    else:
        energy_accumulated = energy_data["energy-accumulated"]
        amount_trigger = KW_H
        csv_functions.delete_file_csv(LAST_RECORD_TRIGGER)

    #Si hay un archivo de api backup pendiente a enviar, envía al Backend
    if(csv_functions.isExistsFile(f"{BACKUP_FILES_DIR}/{BACKUP_FILE_ENERGY_DATA}")):
        rest.send_batch_energy_data()

    rest.save_energy_data(energy_data) #Save energy data to backend
    if(energy_accumulated >= amount_trigger or csv_functions.isExistsFile(f"{BACKUP_FILES_DIR}/{BACKUP_FILE_ROBONOMICS}")):
        energy_remainder = energy_accumulated - amount_trigger
        csv_functions.save_last_trigger_meter(energy_data, energy_remainder)
        logging.info("Starting Connection to Robonomics.")
        try:
            
            last_data_log = data_log.get_item(account_with_seed.get_address())
            last_energy_accumulated_robo = last_data_log[1] if last_data_log else 0
            energy_data["energy-accumulated"] = last_energy_accumulated_robo + energy_accumulated # Set energy accumulated of robonomics
            
            # Si hay un archivo pendiente con registros pendiente a enviar a la red de robonomics
            if(csv_functions.isExistsFile(f"{BACKUP_FILES_DIR}/{BACKUP_FILE_ROBONOMICS}")):
                robonomics_backup = csv_functions.csvToArrayJson()
                csv_functions.delete_file_csv(BACKUP_FILE_ROBONOMICS)
                threads = list()
                for key in robonomics_backup:
                    t = threading.Thread(target=data_log.record(json.dumps(key)), args=())
                    threads.append(t)
                    t.start()

            data_log.record(json.dumps(energy_data))
            logging.info(f"Successfully logged data log in robonomics! {energy_data}")
        except Exception as e:
            logging.error(f"Failed to record Datalog in Robonomics: {e}")
            csv_functions.append_data_grid(BACKUP_FILE_ROBONOMICS, energy_data)
    else:
        logging.info(f"Missing power for registration to robonomics {amount_trigger - energy_accumulated} Wh") 
    logging.info("Robonomics session finished.")    
    logging.info("Session over.")
    time.sleep(EACH_NUMBER_MINUTES)