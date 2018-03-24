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

IP = "127.0.0.1" 
#input('Inserte la IP a donde desea conectar la aplicacion (local - 127.0.0.1, remoto - 0.0.0.0): ')

PORT = 8081
#int(input('Inserte el puerto en el que desea escuchar conexiones: '))

dir_servidor = (IP, PORT)
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServidor.bind(dir_servidor)
TAM_BUFFER = 4096
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
	
	#recibe el nombre del archivo
	data, addr = socketServidor.recvfrom(TAM_BUFFER)
	nombre_archivo = data.strip()
	
	#dir, ip y puerto
	dir_cliente = addr
	
	os.chdir(dir_archivos)
	f=open(nombre_archivo, 'rb')
	socketCliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	while data:
		#dataEnv contiene en [0] el mensaje y en [1] el mensaje hasheado
		dataEnv = []
		dataEnv.append(f.read(TAM_MSG))
		hash_object = hashlib.md5(dataEnv[0])
		dataEnv.append(hash_object.hexdigest())
		print(str(dataEnv[1]))
		if socketCliente.sendto(pickle.dumps(dataEnv),addr):
			print('Se esta enviando 1 pedacito')
			try:
				socketServidor.settimeout(3)
				resp, addr = socketServidor.recvfrom(TAM_BUFFER)
				if resp == b'ACK':
					data = f.read(TAM_BUFFER)
			except Exception:
				pass

	socketCliente.close()
	f.close()


def verificarTimeout():
	"""
	Verifica si hay una "sesion" con un cliente (ip) que expiro.
	El tiempo de expiracion (timeout) es de 5 segundos.
	Cada dos segundos se verifica el timeout de todos los clientes.
	"""
	while True:
		time.sleep(2)
		print('Clientes enviando:{}'.format(tiempos))
		tiempo_comparacion = time.time()
		with lock:
			for ip in list(tiempos):
				tiempo_comparacion = abs(tiempo_comparacion - tiempos[ip][0])
				if tiempo_comparacion > 5:
					#Se deben imprimir las estadisticas en el archivo:
					num_recibidos = tiempos[ip][1]
					num_esperados = tiempos[ip][2]
					num_perdidos = num_esperados - num_recibidos
					nombretxt = str(ip) + ".txt"
					promedio = (tiempos[ip][3])/num_esperados
					os.chdir(dir_data)
					file = open(nombretxt,"a")
					file.write('Transferencia terminada. Recibidos: {}. Total esperados: {}. Perdidos: {}. Promedio tiempo envio: {}\n'.format(num_recibidos, num_esperados, num_perdidos, promedio))
					file.close()
					os.chdir(dir_src)
					del tiempos[ip]




if __name__ == "__main__":
	lock = threading.RLock()
	thread_enviarObjetos = threading.Thread(
		target = enviarObjetos
	)
	thread_enviarObjetos.start()
	#verificarTimeout()
