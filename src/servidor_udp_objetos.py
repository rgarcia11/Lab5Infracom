"""
servidor
"""
#imports
import socket
import pickle
import time
import threading
import os
#datos
#IP = '127.0.0.1'
#PORT = 5010
IP = input('Inserte la IP a donde desea conectar la aplicacion: ')
PORT = int(input('Inserte el puerto en el que desea escuchar conexiones: '))
dir_servidor = (IP, PORT)
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServidor.bind(dir_servidor)
TAM_BUFFER = 1024
dir_src = os.getcwd()
dir_data = os.path.join(dir_src[:-(len(os.sep)+len("src"))],"data")

class ObjetoEnviar():
	"""
	Esta clase hace un objeto...
	"""
	def __init__(self, numSecuencia0, marcaTiempo0, totalArchivos0):
		"""
		Este metodo nanan
		"""
		#este el numero de la secuencia
		self.numSecuencia = numSecuencia0
		self.marcaTiempo = marcaTiempo0
		self.totalArchivos = totalArchivos0
		
	def darSecuencia(self):
		return self.numSecuencia
		
	def darMarcaTiempo(self):
		return self.marcaTiempo
	
	def darTotalObjetos(self):
		return self.totalArchivos

def recibirObjetos():
	while True:
		data, addr = socketServidor.recvfrom(TAM_BUFFER)
		tiempo_recepcion = time.time()
		ip = addr[0]
		port = addr[1]
		
		
		data = pickle.loads(data)
		#print(data.darSecuencia(), data.darMarcaTiempo())		

		#tiempo actual - tiempo de envio = tiempo en segundos de la transferencia, *1000 para ms
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
		

"""
tiempos[ip][data]
	ip[###]: la ip del cliente que envio el mensaje
	data[0]: timestamp en el que se recibio el paquete
	data[1]: contador de objetos recibidos hasta el momento
	data[2]: total de objetos a mandar por parte del cliente
"""
tiempos = {}

lock = threading.RLock()
thread_recibirObjetos = threading.Thread(
	target = recibirObjetos
)
thread_recibirObjetos.start()

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
			
##Revisar los tiempos del arreglo tiempos



cont =0

	
#C:\Users\ale_e\Desktop\Alejandro\UNIVERSIDAD ANDES\6to Semestre (Local)\Infraestructura de Comunicaciones\Lab5\Lab5Infracom