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
import socket
import time 

from logging_utils import *
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from collections import deque
from threading import Thread
from random import choice

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

input_data = deque() # deque is thread safe for pop U popleft U append

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
WS_URL = cp.get("websocket", "ws_url") or "websocket"
DEBUG = cp.getboolean("self", "debug")
RELOAD = cp.getboolean("self", "reload")
VERBOSE = cp.getboolean("self","verbose")

S_HOST = cp.get("socket", "host")
S_PORT = cp.get("socket", "port")
S_MAX_CONNECTIONS = cp.get("socket", "max_connections")

SIMULATION = False
SIMULATION_DATA_URL = None
SIMULATION_DATA = None

"""
  __________
< SIMULATION >
  ----------
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\
                 ||----w |
                 ||     ||

"""

def simulation_worker( data ):
	while True:
		to_append = choice(data)
		input_data.append(to_append)
		log(VERBOSE, "[{0}]\t [simulation] : INCOMING DATA : {1}".format(SCRIPT_NAME, to_append) )
		time.sleep( choice( range(1,6) ) )

if S_HOST == "None" or S_PORT == "None":
	SIMULATION = True
	SIMULATION_DATA_URL = cp.get("simulation", "data_path")
	log(VERBOSE, "[{0}]\tSIMULATION ACTIVE".format(SCRIPT_NAME))
	log(VERBOSE, "[{0}]\tusing feed:\t{1}".format(SCRIPT_NAME, SIMULATION_DATA_URL))

	with open(SIMULATION_DATA_URL, "r") as fp:
		SIMULATION_DATA = fp.readlines()

if SIMULATION:
	simulation_job = Thread(target=simulation_worker, args=[SIMULATION_DATA])
	simulation_job.daemon = True
	simulation_job.start()

if not SIMULATION:
	input_socket = socket.socket()
	input_socket.bind( ("", int(S_PORT) ))
	log(VERBOSE, "[{0}]\tINPUT SOCKET BINDED TO PORT {1}".format(SCRIPT_NAME, S_PORT))
	input_socket.listen(S_MAX_CONNECTIONS)


"""
  ______
< WEBAPP >
  ------
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\
                 ||----w |
                 ||     ||

"""

app = bt.Bottle()

# WEBSOCKET SERVER
@app.route("/"+WS_URL, apply=[websocket])
def route_websocket(ws):
	while True:
		try:
			ws.send(input_data.popleft()) # THREAD SAFE :)
		except Exception as e:
			log(DEBUG, "[{0}]\t : ERROR : {1}".format(SCRIPT_NAME, e) )
			time.sleep(0.1)



# WEBSOCKET CLIENT
@app.route("/simulation_client")
def route_view_simulation():
	return bt.template('client', url=WS_URL, host=HOST, port=PORT)


"""
  ______
< TESTS >
  ------
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\
                 ||----w |
                 ||     ||
"""

# ECHO WEBSOCKET SERVER SIDE
@app.route("/echo", apply=[websocket])
def route_ws_echo(ws):
	while True:
		msg = ws.receive()
		if msg is not None:
			ws.send(msg)
		else:
			break

# ECHO WEBSOCKET CLIENT
@app.route("/echo_client")
def route_view_echo():
	return bt.template('echo_client')


# INSPECT INPUT_DATA
@app.route("/input_data")
def route_inspect_data():
	return str(input_data)

app.run( host=HOST, port=PORT, debug=DEBUG, reloader=RELOAD, server=GeventWebSocketServer )