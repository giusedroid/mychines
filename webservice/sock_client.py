import socket
import time
from random import choice

HOST = "localhost"
PORT = 8081

output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
output_socket.connect((HOST, PORT))

while True:

	message = "Hello. Is there anybody out there?"
	output_socket.sendall(message)
	time.sleep(choice(range(6)))
