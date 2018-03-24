"""
Cliente UDP

Recibe archivos del servidor UDP que se especifica por consola.

"""

import socket
import time
import pickle
import hashlib
from ObjetoEnviar import *


#Definicion de ip y puerto del servidor, socket para establecer comunicacion y direccion del servidor.
IP = "127.0.0.1" 
#input('Inserte la IP a la que desea conectarse: ')

PORT = 8081
#int(input('Inserte el puerto al que desea conectarse'))"""

nombre_archivo = "test.pdf"
#input('Inserte nombre del archivo a pedir.')"""

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dir_servidor = (IP, PORT)
TAM_BUFFER = 4096
ACK = 'ACK'
NAC = 'NAC'
def pedirArchivo(nombre_archivo):
	"""
	Pide un archivo al servidor.
	1--Envia un mensaje al servidor con el archivo a pedir.
	2--Recibe archivos en un while.
	 --La condicion del while es que no se reciba nulo.
	3--La condicion real de salida es el timeout del socket
	 --Se establece un timeout de 3 segundos al socket
	4--Cuando se cumple el timeout (se captura la excepcion)
	   y se termina de transferir.
	args:
		nombre_archivo: nombre del archivo a pedir
	"""
	
	#crea el archivo vacio donde se va a escribir lo que se recibe del servidor
	f = open(nombre_archivo, 'wb')
	
	#envia al servidor nombre del archivo a descargar
	servidor.sendto(nombre_archivo.encode(), dir_servidor)
	fallo = 0
	try:
		servidor.settimeout(5)
		data,addr = servidor.recvfrom(TAM_BUFFER)
		data = pickle.loads(data)
		servidor.sendto(ACK.encode(), dir_servidor)
	except:
		fallo = 1
		print('El servidor no respondio.')

	if not fallo:
		try:
			while True:
				f.write(data[0])
				servidor.settimeout(3)
				data,addr = servidor.recvfrom(TAM_BUFFER)
				data = pickle.loads(data)
				hash_object = hashlib.md5(data[0])
				if hash_object.hexdigest() == data[1]:
					servidor.sendto(ACK.encode(), dir_servidor)
				else:
					servidor.sendto(NAC.encode(), dir_servidor)
		except:
			f.close()
			servidor.close()
			print('Termino de transferir')

if __name__ == "__main__":
	pedirArchivo(nombre_archivo)
