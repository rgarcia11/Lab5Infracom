"""
cliente
"""

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
	
objetos	= 5
i = 0
while i < objetos:
	objeto = ObjetoEnviar(i, time.now())