"""
Cliente UDP

Recibe archivos del servidor UDP que se especifica por consola.

"""

import socket
import time
import pickle
from ObjetoEnviar import *

#Definicion de ip y puerto del servidor, socket para establecer comunicacion y direccion del servidor.
IP = input('Inserte la IP a la que desea conectarse: ')
PORT = int(input('Inserte el puerto al que desea conectarse'))
nombre_archivo = input('Inserte nombre del archivo a pedir.')
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dir_servidor = (IP, PORT)
TAM_BUFFER = 1024
def pedirArchivo(nombre_archivo):
	"""
	Pide un archivo al servidor
	args:
		nombre_archivo: nombre del archivo a pedir
	"""
	f = open(nombre_archivo, 'wb')
	servidor.sendto(nombre_archivo.encode(), dir_servidor)
	data,addr = servidor.recvfrom(TAM_BUFFER)
	try:
		while data:
			f.write(data)
			servidor.settimeout(3)
			data,addr = servidor.recvfrom(TAM_BUFFER)
	except:
		f.close()
		servidor.close()
		print('Termino de transferir')

if __name__ == "__main__":
	pedirArchivo(nombre_archivo)
