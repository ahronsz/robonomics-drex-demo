import os
import datetime, calendar
import errno
import shutil
import struct
import time
import requests
from dotenv import load_dotenv

load_dotenv()
BACKUP_FILES_DIR = os.getenv('BACKUP_FILES_DIR')
BACKUP_FILE_ROBONOMICS = os.getenv('BACKUP_FILE_ROBONOMICS')
BACKUP_FILE_API = os.getenv('BACKUP_FILE_API')
MAX_BACKUP_SIZE = int(os.getenv('MAX_BACKUP_SIZE'))

# Trying to create backup files directory
try:
    # Create target Directory
    os.mkdir(BACKUP_FILES_DIR)
    print("[INFO] Directory {} created ".format(BACKUP_FILES_DIR)) 
except OSError as e:
    if e.errno == errno.EEXIST:
        print("[INFO] Directory {} already exists".format(BACKUP_FILES_DIR))

try:
    # Create target Directory
    os.mkdir(PENDING_FILES_DIR)
    print("[INFO] Directory {} created ".format(PENDING_FILES_DIR)) 
except OSError as e:
    if e.errno == errno.EEXIST:
        print("[INFO] Directory {} already exists".format(PENDING_FILES_DIR))