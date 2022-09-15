import logging
import time
import sys
import rest
import rpi_funcs as rpi

from robonomicsinterface import Account
from robonomicsinterface import Datalog
#from substrateinterface import Keypair

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# Define Robonomics sss58_address from seed
seed: str = sys.argv[1]
#keypair = Keypair.create_from_mnemonic(seed, ss58_format=2)
account_with_seed = Account(seed=seed, remote_ws="")

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
        # Initiate RobonomicsInterface instance
        #ri_interface = RI(seed=seed, remote_ws="wss://kusama.rpc.robonomics.network")
        rest.record_log(operation)
        #ri_interface = RI(seed=seed, remote_ws="ws://127.0.0.1:9944")
        datalog = Datalog(account_with_seed)
        datalog.record("Hello, world")
          # If index was not provided here, the latest one will be used
        logging.info(f"Successfully! {datalog.get_item(account_with_seed.get_address())}")
        #ri_interface.record_datalog(f"Successfully! {operation}")
        #if operation["success"]:
        #    print("hola mundo")
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