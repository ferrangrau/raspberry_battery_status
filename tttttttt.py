from datetime import datetime

import os

filename = "/home/fgh/git/altair12/raspberry_battery_status/run_OLD.py"

# if last modification date of the file was one year before, empty file
if os.path.isfile(filename):
    statbuf = os.stat(filename)

    if datetime.fromtimestamp(statbuf.st_mtime).strftime("%m") < datetime.now().strftime("%m"):
        open(filename, 'w').close()

    print(datetime.fromtimestamp(statbuf.st_mtime).strftime("%m"), datetime.now().strftime("%m"))