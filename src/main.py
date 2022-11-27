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
    rpi_read = rpi.get_data_grid()
    rest.record_log(rpi_read)
    try:
        logging.info("Starting Connection to Robonomics.")
        last_data_log = data_log.get_item(account_with_seed.get_address())
        last_data_log = json.loads(last_data_log[1]["energy-accumulated"] if last_data_log else 0.0)
        _energy_accumulated = rpi_read["energy-accumulated"]
        
        current_energy = _energy_accumulated - last_data_log
        if current_energy >= 1000 :
            data_log.record(json.dumps(rpi_read))
            lastDatalog = data_log.get_item(account_with_seed.get_address())  # If index was not provided here, the latest one will be used
            logging.info(f"Successfully logged data log in robonomics! {lastDatalog[1]}")
        
        logging.info("Robonomics session finished.")
    except Exception as e:
        logging.error(f"Failed to record Datalog in Robonomics: {e}")
    logging.info("Session over.")
    time.sleep(20)
