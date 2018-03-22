"""
servidor
"""
#imports
import socket
import pickle
import time

#datos
IP = '127.0.0.1'
PORT = 5010
dir_servidor = (IP, PORT)
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServidor.bind(dir_servidor)
TAM_BUFFER = 1024

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

def recibirObjetos(tiempos):
	global tiempos
	while True:
		data, addr = socketServidor.recvfrom(TAM_BUFFER)
		tiempos[addr[0]] = time.time()
		cont=cont+1
		data = pickle.loads(data)
		print(data)
		print(data.darSecuencia(), data.darMarcaTiempo(), cont)
		
		ip = addr[0]
		port = addr[1]
		
		#tiempo actual - tiempo de envio = tiempo en segundos de la transferencia, *1000 para ms
		tiempo= (time.time()-data.darMarcaTiempo())*1000
		nombretxt = str(ip) + ".txt"
		
		file = open(nombretxt,"a") 
		file.write(str(data.darSecuencia()) +": "+ str(tiempo)+"\n") 
		file.close() 

tiempos = {}
thread_recibirObjetos = threading.Thread(
	target = recibirObjetos,
	args=(evento_timeout,tiempos)
)
thread_recibirObjetos.start()

##Revisar los tiempos del arreglo tiempos



cont =0

	
#C:\Users\ale_e\Desktop\Alejandro\UNIVERSIDAD ANDES\6to Semestre (Local)\Infraestructura de Comunicaciones\Lab5\Lab5Infracom