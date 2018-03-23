class ObjetoEnviar():
	"""
	Objeto que se envia a traves de UDP. Para poder inicializarlo como
	objeto a nivel de servidor, el servidor debe saber que objeto es.
	"""
	def __init__(self, numSecuencia0, marcaTiempo0, totalArchivos0):
		"""
		Inicializa el objeto a enviar.
		args:
			numSecuencia0: numero de secuencia del objeto.
			marcatiempo0: marca de tiempo del momento de creacion del objeto.
			totalArchivos0: total de archivos a ser enviados.
		"""
		self.numSecuencia = numSecuencia0
		self.marcaTiempo = marcaTiempo0
		self.totalArchivos = totalArchivos0
		
	def darSecuencia(self):
		"""
		Retorna el numero de secuencia.
		"""
		return self.numSecuencia
		
	def darMarcaTiempo(self):
		"""
		Retorna la marca de tiempo.
		"""
		return self.marcaTiempo
	
	def darTotalObjetos(self):
		"""
		Retorna el total de objetos a enviar.
		"""
		return self.totalArchivos
