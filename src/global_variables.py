import os
import datetime, calendar
from dotenv import load_dotenv

load_dotenv()
SEED = os.getenv('SEED') #Define Panel solar machine Robonomics account
KW_H = int(os.getenv('KW_H')) #Define the amount of kilowatts per hour to arrive to trigger the sending to robonomics
BACKUP_FILES_DIR = os.getenv('BACKUP_FILES_DIR')
BACKUP_FILE_ENERGY_DATA = os.getenv('BACKUP_FILE_ENERGY_DATA')
BACKUP_FILE_ROBONOMICS = os.getenv('BACKUP_FILE_ROBONOMICS')
LAST_RECORD_TRIGGER = os.getenv('LAST_RECORD_TRIGGER')
BASE_URL_BACKEND_CONSUME = os.getenv('BASE_URL_BACKEND_CONSUME')
EACH_NUMBER_MINUTES = int(os.getenv('EACH_NUMBER_MINUTES'))
#MAX_BACKUP_SIZE = int(os.getenv('MAX_BACKUP_SIZE'))

#current posix timestamp
def currentTimestamp():
    return calendar.timegm(datetime.datetime.utcnow().utctimetuple()) * 1000