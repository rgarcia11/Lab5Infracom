"""
Servidor UDP.

Envia archivos por un datagrama (UDP).

"""

import socket
import pickle
import time
import threading
import os
import hashlib
from ObjetoEnviar import *

#Ip, puerto, inicializacion de socket, tamanho del buffer y direccion de carpetas
#IP = "127.0.0.1"
IP = input('Inserte la IP a donde desea conectar la aplicacion (local - 127.0.0.1, remoto - 0.0.0.0): ')
#PORT = 8081
PORT = int(input('Inserte el puerto en el que desea escuchar conexiones: '))

#Params iniciales
dir_servidor = (IP, PORT)
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServidor.bind(dir_servidor)
TAM_BUFFER = 1048576
TAM_MSG = 1024
dir_src = os.getcwd()
dir_data = os.path.join(dir_src[:-(len(os.sep)+len("src"))],"data")
dir_archivos = os.path.join(dir_src[:-(len(os.sep)+len("src"))],"archivos")


tiempos = {}

def enviarObjetos():
	"""
	Envia objetos.
	1--Se recibe un mensaje del cliente que contiene:
		data: el nombre del archivo
		addr: la direccion (ip y puerto) del cliente.
			Se utilizara addr para responderle a ese cliente.
	"""

	#recibe el nombre del archivo y lo pasa devuelta a string
	data, addr = socketServidor.recvfrom(TAM_BUFFER)
	nombre_archivob = data.strip()
	nombre_archivo = nombre_archivob.decode()

	print(nombre_archivo)

	#dir, ip y puerto
	dir_cliente = addr

	os.chdir(dir_archivos)
	f=open(nombre_archivo, 'rb')
	socketCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	#  -- algunas variables ---
	condicionG = True # dice si acabo de enviar
	contador = 0 # cuenta la cantidad de paquetes enviados con respuesta de que llegaron bien
	leerNuevo = True # dice si hay que leer mas de el archivo para reenviar (TRUE) o si es necesario reenviar (FALSE)
	dataEnv = [] #dataEnv contiene en [0] el mensaje en bytes y en [1] el mensaje hasheado como un string
	#  -------

	while condicionG: # si no hay nada que enviar termina
		if leerNuevo:
			# solo se cambian los datos a enviar
			dataEnv[:]=[]
			dataEnv.append(f.read(TAM_MSG)) #Guarda la porcion del archivo (datos) a mandar en el paquete
			if dataEnv[0]:
				#Guarda el hash del mensaje para verificacion de integridad
				hash_object = hashlib.md5(dataEnv[0])
				dataEnv.append(hash_object.hexdigest())
				#print("data:"+ str(dataEnv[0]) + " hash: " + dataEnv[1])
			else:
				condicionG = False
		if condicionG:
			#envia dataEnv con pickle al addr(puerto & ip)
			socketCliente.sendto(pickle.dumps(dataEnv), addr)
			print('Se envio 1 paquete')
			try:
				socketServidor.settimeout(2)
				resp, addr = socketServidor.recvfrom(TAM_BUFFER)
				if resp == b'ACK':
					contador = contador + 1
					leerNuevo = True
					#print('Se recibio respuesta ACK ! bien')
				else:
					leerNuevo = False #El paquete le llego corrupto
					#print('Se recibio respuesta NAC')
			except Exception:
				print('No se recibio ACK')
				leerNuevo = False  #El paquete no llego, se perdio la respuesta o el cliente no esta conectado
	socketCliente.close()
	f.close()

if __name__ == "__main__":
	lock = threading.RLock()
	thread_enviarObjetos = threading.Thread(
		target = enviarObjetos
	)
	thread_enviarObjetos.start()


#C:\Users\ale_e\Desktop\Alejandro\UNIVERSIDAD ANDES\6to Semestre (Local)\Infraestructura de Comunicaciones\Lab5\Lab5Infracom\src
