import socket
import time

HOST = "192.168.1.77"
PORT = 8081

input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
input_socket.bind( (HOST, PORT) )
input_socket.listen(5)

while True:
	connection, address = input_socket.accept()
	data = connection.recv(4096)
	print data
	connection.close()

