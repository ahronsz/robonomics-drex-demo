import logging
import time
import json
import sys
import rest
import rpi_funcs as rpi

from robonomicsinterface import Account, Datalog

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# Define Robonomics sss58_address from seed
seed: str = sys.argv[1]
account_with_seed = Account(seed=seed, remote_ws="ws://127.0.0.1:9944")

# Start solar panel daemon
logging.info("Started main Solar panel daemon")
while True:
    try:
        datalog = Datalog(account_with_seed)
        lastDatalog = datalog.get_item(account_with_seed.get_address())
        rpiLog = rpi.get_log()
        rest.record_log(rpiLog)
        json_lastDatalog = json.loads(lastDatalog[1])

        last_energy_robo = json_lastDatalog["energy-acum"] if json_lastDatalog["energy-acum"] else 0
        current_energy_rpi = rpiLog["energy-acum"] if rpiLog["energy-acum"] else 0
        current_energy = current_energy_rpi - last_energy_robo    
        if current_energy >= 10000 :
            datalog.record(json.dumps(rpiLog))
            lastDatalog = datalog.get_item(account_with_seed.get_address())  # If index was not provided here, the latest one will be used
            logging.info(f"Successfully logged datalog in robonomics! {lastDatalog[1]}")
        else :
            logging.info(f"Missing power for registration to robonomics {current_energy} Kw") 
    except Exception as e:
        logging.error(f"Failed to record Datalog: {e}")
    logging.info("Session over")
    time.sleep(60)