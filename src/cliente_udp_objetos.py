"""
Cliente UDP

Envia objetos al servidor UDP que se especifica por consola.
"""

import socket
import time
import pickle
from ObjetoEnviar import *

#Definicion de ip y puerto del servidor, socket para establecer comunicacion y direccion del servidor.
IP = input('Inserte la IP a la que desea conectarse: ')
PORT = int(input('Inserte el puerto al que desea conectarse'))
objetos = int(input('Inserte numero de objetos a enviar.'))
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dir_servidor = (IP, PORT)

def enviarObjetos(objetos):
	"""
	Envia al servidor el numero de objetos que entra por parametro.
	args:
		objetos: numero de objetos a enviar.
	"""
	i = 0
	while i < objetos:
		objeto = ObjetoEnviar(i, time.time(), objetos)
		print('Objeto original  . sec: {}, marca: {}'.format(objeto.darSecuencia(), objeto.darMarcaTiempo()))
		servidor.sendto(pickle.dumps(objeto), dir_servidor)
		i = i+1
	
if __name__ == "__main__":
	enviarObjetos(objetos)