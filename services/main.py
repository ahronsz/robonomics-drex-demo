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

# Define Panel solar machine Robonomics account
seed: str = sys.argv[1]
account_with_seed = Account(seed=seed, remote_ws="wss://rococo.rpc.robonomics.network:9944")
datalog = Datalog(account_with_seed)

# Start solar panel daemon
logging.info("Started main Solar panel daemon")
while True:
    try:
        
        lastDatalog = datalog.get_item(account_with_seed.get_address())
        rpiLog = rpi.get_log()
        datalog.record(json.dumps(rpiLog))
        lastDatalog = datalog.get_item(account_with_seed.get_address())  # If index was not provided here, the latest one will be used
        logging.info(f"Successfully logged datalog in robonomics! {lastDatalog[1]}")
        #rest.record_log(rpiLog)
        #json_lastDatalog = json.loads(lastDatalog[1] if lastDatalog else """{"energy-acum": 0}""")

        #last_energy_robo = json_lastDatalog["energy-acum"]
        #current_energy_rpi = rpiLog["energy-acum"] if rpiLog else 0
        #current_energy = current_energy_rpi - last_energy_robo
        #if current_energy >= 1000 :
            
        #else :
        #    logging.info(f"Missing power for registration to robonomics {1000 if current_energy == 0 else round(1000 - current_energy, 2)} Wh") 
    except Exception as e:
        logging.error(f"Failed to record Datalog: {e}")
    logging.info("Session over")
    time.sleep(5)
