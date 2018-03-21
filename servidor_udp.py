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

class ObjetoEnviar():
	"""
	Esta clase hace un objeto...
	"""
	def __init__(self, numSecuencia0, marcaTiempo0):
		"""
		Este metodo nanan
		"""
		#este el numero de la secuencia
		self.numSecuencia = numSecuencia0
		self.marcaTiempo = marcaTiempo0
		
		
	def darSecuencia(self):
		return self.numSecuencia
		
	def darMarcaTiempo(self):
		return self.marcaTiempo



cont =0
while True:
	data, addr = socketServidor.recvfrom(TAM_BUFFER)
	cont=cont+1
	data = pickle.loads(data)
	print(data)
	print(data.darSecuencia(), data.darMarcaTiempo(), cont)
	
#C:\Users\ale_e\Desktop\Alejandro\UNIVERSIDAD ANDES\6to Semestre (Local)\Infraestructura de Comunicaciones\Lab5\Lab5Infracom