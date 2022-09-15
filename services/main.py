import logging
import time
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
    #if operation["success"]:
    logging.info("Operation Successful.")
    try:
        operation = rpi.get_log()
        rest.record_log(operation)
        datalog = Datalog(account_with_seed)
        datalog.record(f"Successfully! {operation}")
        lastDatalog = datalog.get_item(account_with_seed.get_address())  # If index was not provided here, the latest one will be used
        logging.info(f"Successfully! {lastDatalog.get}")
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