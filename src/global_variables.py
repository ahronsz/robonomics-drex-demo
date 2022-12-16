import os
import datetime, calendar
from dotenv import load_dotenv

load_dotenv()
DEVICE_CODE = os.getenv('DEVICE_CODE')
EACH_MINUTE = int(os.getenv('EACH_MINUTE'))
BACKUP_FILES_DIR = os.getenv('BACKUP_FILES_DIR')
BACKUP_FILE_ENERGY_DATA = os.getenv('BACKUP_FILE_ENERGY_DATA')
BASE_URL_BACKEND_CONSUME = os.getenv('BASE_URL_BACKEND_CONSUME')

#current posix timestamp
def currentTimestamp():
    return calendar.timegm(datetime.datetime.utcnow().utctimetuple()) * 1000