"""
cliente
"""
#Imports
import socket
import time
import pickle
#Datos importantes
IP = "127.0.0.1"
PORT = 5010
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dir_servidor = (IP, PORT)

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


objetos	= 1
i = 0
while i < objetos:
	objeto = ObjetoEnviar(i, time.time())
	print('Objeto original  . sec: {}, marca: {}'.format(objeto.darSecuencia(), objeto.darMarcaTiempo()))
	objectoB = pickle.dumps(objeto)
	objetoR = pickle.loads(objectoB)
	print('Objeto recuperado. sec: {}, marca: {}'.format(objetoR.darSecuencia(), objetoR.darMarcaTiempo()))
	#servidor.sendto(file,dir_servidor)
	servidor.sendto(pickle.dumps(objeto), dir_servidor)
	i = i+1







