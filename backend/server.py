"""
  _______
< IMPORTS >
  -------
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\
                 ||----w |
                 ||     ||
"""

import bottle as bt
import ConfigParser
import sys
import json
import time 
from random import choice
from logging_utils import *
from threading import Thread

"""
  _________________
< IMPORTANT VALUES >
  -----------------
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\
                 ||----w |
                 ||     ||
    
"""

SCRIPT_NAME = sys.argv[0]

try:
	CONFIG_PATH = sys.argv[1]
except Exception as e:
	CONFIG_PATH = "config/default"

"""
  ______________
< CONFIGURATIONS >
  --------------
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\
                 ||----w |
                 ||     ||

"""

cp = ConfigParser.ConfigParser()

try:
	cp.read(CONFIG_PATH)
except Exception as e:
	log(True, "[{0}]\t[FATAL ERROR]\tCould not read or parse configuration file {1}".format(SCRIPT_NAME, CONFIG_PATH))
	exit(-1)

HOST = cp.get("self", "host")
PORT = cp.get("self", "port")
DEBUG = cp.getboolean("self", "debug")
RELOAD = cp.getboolean("self", "reload")
VERBOSE = cp.getboolean("self","verbose")

SIMULATION_PATH = cp.get("simulation","data_path")

with open(SIMULATION_PATH,"r") as fp:
	DATA = json.loads(fp.read())

def data_worker():
	while True:
		DATA['time'] = time.time()
		DATA['jobRequests'] = choice(xrange(50,100))
		DATA['doneJobs'] = choice(xrange(10,DATA['jobRequests'])) 
		DATA['failedJobs'] = choice(xrange(0, DATA['jobRequests'] - DATA['doneJobs'] ) )
		DATA['refusedJobs'] = choice(xrange(0, DATA['jobRequests'] - DATA['failedJobs'] - DATA['doneJobs'] ) )
		DATA['totCreatedVM'] = choice(xrange(1,20))
		DATA['trustMatrixDecrements'] = choice(xrange(10,200))
		DATA['trustMatrixVariations'] = choice(xrange(10,200))
		DATA['trustMatrixIncrements'] = choice(xrange(10,200))
		time.sleep(1)

data_job = Thread(target=data_worker)
data_job.daemon = True
data_job.start()


app = bt.Bottle()

@app.route("/data")
def get_data():
	return json.dumps(DATA)

app.run( host=HOST, port=PORT, debug=DEBUG, reloader=RELOAD )

