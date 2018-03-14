"""
"""
#imports
import socket
import pickle
#datos
IP = '127.0.0.1'
PORT = 5010
dir_servidor = (IP, PORT)
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServidor.bind(dir_servidor)
TAM_BUFFER = 1024

while True:
	data = pickle.loads(socketServidor.recv(TAM_BUFFER))
	print(data)
	#data, addr = sock.recvfrom(TAM_BUFFER)