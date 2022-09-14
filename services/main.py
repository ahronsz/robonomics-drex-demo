import logging
import time
import sys
import rest
import rpi_funcs as rpi

from robonomicsinterface import RobonomicsInterface as RI
from statemine_monitor import DrxIncomeTracker
from substrateinterface import Keypair

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# Define Statemine sss58_address from seed
t=10 #seconds
seed: str = sys.argv[1]
keypair = Keypair.create_from_mnemonic(seed, ss58_format=2)

# Start income tracker
#income_tracker = DrxIncomeTracker(keypair.ss58_address)

# Start solar panel daemon
logging.info("Started main Solar panel daemon")
while True:
    # wait for money income event
    #income_tracker.act_income_event.wait()
    #income_tracker.act_income_event.clear()
    

    #if operation["success"]:
    logging.info("Operation Successful.")
    try:
        operation = rpi.get_log()
        logging.info(f"Successfully! {operation}")
        # Initiate RobonomicsInterface instance
        #ri_interface = RI(seed=seed, remote_ws="wss://kusama.rpc.robonomics.network")
        rest.record_log(operation)
        #ri_interface = RI(seed=seed, remote_ws="ws://127.0.0.1:9944")
        #ri_interface.record_datalog(f"Successfully! {operation}")
    except Exception as e:
        logging.error(f"Failed to record Datalog: {e}")
    #else:
        #logging.error(f"Operation Failed.")
        #try:
            # Initiate RobonomicsInterface instance
            #ri_interface = RI(seed=seed, remote_ws="wss://kusama.rpc.robonomics.network")
            #ri_interface.record_datalog(f"Failed: {operation['message']}")
        #except Exception as e:
            #logging.error(f"Failed to record Datalog: {e}")
    logging.info("Session over")
    time.sleep(60)