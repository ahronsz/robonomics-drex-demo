'''
░░░░░░░░░░░░░░░░░░░░██████╗░░██████╗░░███████╗░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     
░░░░░░░░░░░░░░░░░░░░██╔══██╗░██╔══██╗░██╔════╝░█╗░░░█╗░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░██║░░██║░██████╔╝░█████╗░░░░█║░█╔╝░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░██║░░██║░██╔══██╗░██╔══╝░░░░░██═╝░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░██████╔╝░██║░░██║░███████╗░░█╔═█╗░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░█████╔╝░░██║░░██║░███████║░█╔╝░░█╗░░░░░░░░░░░░░░░░░░░░░░░░░░
'''
import logging
import time
import json
import sys
import expose.rest as rest
import rpi_funcs as rpi
import grid_data as backup
from global_variables import *

from robonomicsinterface import Account, Datalog

sys.dont_write_bytecode = True
# set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# Define Panel solar machine Robonomics account
_seed: str = sys.argv[1]
try:
    account_with_seed = Account(seed=_seed, remote_ws="ws://127.0.0.1:9944")
    data_log = Datalog(account_with_seed)
except Exception as e:
    logging.error(e)
    raise SystemExit

# Start solar panel daemon
logging.info("Started main Solar panel daemon.")

while True:
    energy_data = rpi.get_data_grid()
    rest.record_log(energy_data)
    if(energy_data["energy-acum"] >= backup.get_last_trigger_meter + 1000):
        backup.save_last_trigger_meter(energy_data)
        try:
            logging.info("Starting Connection to Robonomics.")
            last_data_log = data_log.get_item(account_with_seed.get_address())
            last_energy_accumulated_robo = last_data_log[1] if last_data_log else 0
            energy_data["energy-acum"] = last_energy_accumulated_robo + energy_data["energy-acum"]
            data_log.record(json.dumps(energy_data))
        except Exception as e:
            backup.append_data_grid(BACKUP_FILE_ROBONOMICS, energy_data)
            logging.error(f"Failed to record Datalog in Robonomics: {e}")
    logging.info("Robonomics session finished.")    
    logging.info("Session over.")
    time.sleep(20)
            
