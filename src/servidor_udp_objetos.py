"""
Servidor UDP.

Recibe objetos por un datagrama (UDP).
Imprime información asociada a dichos objetos en un archivo de texto en .data/
"""

import socket
import pickle
import time
import threading
import os
from ObjetoEnviar import *

#Ip, puerto, inicializacion de socket, tamanho del buffer y direccion de carpetas
IP = input('Inserte la IP a donde desea conectar la aplicacion (local - 127.0.0.1, remoto - 0.0.0.0): ')
PORT = int(input('Inserte el puerto en el que desea escuchar conexiones: '))
dir_servidor = (IP, PORT)
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServidor.bind(dir_servidor)
TAM_BUFFER = 1024
dir_src = os.getcwd()
dir_data = os.path.join(dir_src[:-(len(os.sep)+len("src"))],"data")

"""
Aclaraciones de convencion sobre el diccionario que contiene la
informacion sobre objetos recibidos de un cliente (ip).
Este diccionario es la comunicacion entre los dos threads que
componen al servidor.
tiempos[ip][data]
	ip[###]: la ip del cliente que envio el mensaje
	data[0]: timestamp en el que se recibio el paquete
	data[1]: contador de objetos recibidos hasta el momento
	data[2]: total de objetos a mandar por parte del cliente
"""
tiempos = {}

def recibirObjetos():
	"""
	Recibe objetos. Esta funcion bloquea el thread que la corra
	porque contiene un while True:
	"""
	while True:
		data, addr = socketServidor.recvfrom(TAM_BUFFER)
		tiempo_recepcion = time.time()
		ip = addr[0]
		port = addr[1]
		
		data = pickle.loads(data)	

		tiempo= (time.time()-data.darMarcaTiempo())*1000
		nombretxt = str(ip) + ".txt"
		os.chdir(dir_data)
		file = open(nombretxt,"a") 
		file.write(str(data.darSecuencia()) +": "+ str(tiempo)+" ms \n") 
		file.close() 
		os.chdir(dir_src)
		
		with lock:
			if ip in tiempos:
				tiempos[ip] = tiempo_recepcion, tiempos[ip][1]+1, tiempos[ip][2], tiempos[ip][3]+tiempo
			else:
				tiempos[ip] = tiempo_recepcion, 1, data.darTotalObjetos(), tiempo
		

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
					#Timeout del cliente  con ip
					#Se deben imprimir las estadisticas en el archivo:
					num_recibidos = tiempos[ip][1]
					num_esperados = tiempos[ip][2]
					num_perdidos = num_esperados - num_recibidos
					nombretxt = str(ip) + ".txt"
					promedio = (tiempos[ip][3])/num_esperados
					os.chdir(dir_data)
					file = open(nombretxt,"a")
					file.write('Archivo terminado. Recibidos: {}. Total esperados: {}. Perdidos: {}. Promedio tiempo envio: {}\n'.format(num_recibidos, num_esperados, num_perdidos, promedio))
					file.close()
					os.chdir(dir_src)
					del tiempos[ip]
	



if __name__ == "__main__":
	lock = threading.RLock()
	thread_recibirObjetos = threading.Thread(
		target = recibirObjetos
	)
	thread_recibirObjetos.start()
	verificarTimeout()

