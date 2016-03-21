import socket
import time
from threading import Thread
import bottle as bt

from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

HOST = "localhost"
PORT = 8088

input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
input_socket.bind( (HOST, PORT) )
input_socket.listen(5)

print "binded to {0}:{1}".format(HOST, PORT)

def worker():
	try:
		while True:
			connection, address = input_socket.accept()
			while True:
				data = connection.recv(4096)
				print data
				if data == "q":
					break
			connection.close()
	except Exception as e:
		print e

job = Thread(target=worker)
job.daemon = False
job.start()


app = bt.Bottle()



def server_worker():
	app.run(host='localhost', port=16051,  reloader=True)


server_job = Thread(target=server_worker)
server_job.daemon = False
server_job.start()