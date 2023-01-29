import socket
import time
import os

EOC = '\x1b[0m'
WHITE = '\x1b[1;37;40m'
GREEN = '\x1b[0;32;40m'
RED = '\x1b[1;31;40m'

filename = r'res/history.txt'

with open(filename, 'r') as h:
	all_lines = len(h.readlines())

printed = False
server_address = ('localhost', 10000)

while True:
	try:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect(server_address)
		print(f"{GREEN}[INFO] {WHITE}Game found.{EOC}")
		break
	except ConnectionRefusedError:
		print(f"{GREEN}[INFO] {RED}Game not found{WHITE}, reconnection in 2 seconds...{EOC}")
		time.sleep(2)

while True:
	try:
		with open(filename, 'r') as h:
			new_lines = len(h.readlines())
		with open(filename, 'r') as h:
			history = h.readlines()[-1]
		if new_lines > 30:
			with open(filename, 'r') as fin:
				data = fin.readlines()
			with open(filename, 'w') as fout:
				fout.write(data[-1])
		if all_lines < new_lines and not printed:
			print(history[:-1])
			printed = True
		with open(filename, 'r') as h:
			h.seek(0, os.SEEK_END)
		printed = False
		all_lines = new_lines
		time.sleep(0.1)
		client_socket.send(b'ping')
	except (BrokenPipeError, ConnectionResetError):
		print(f"{GREEN}[INFO] {WHITE}You left the game.{EOC}")
		client_socket.close()
		break