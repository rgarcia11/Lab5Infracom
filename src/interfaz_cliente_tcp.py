import tkinter as tk
from cliente_tcp import *
import threading
import math
"""
Interfaz del cliente para manejar las interacciones del usuario.
"""
class Application(tk.Frame):
	"""
	Esta clase genera una interfaz
	"""
    def __init__(self, master=None):
		"""
		Constructor
		"""
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
		"""
		Crea todos los elementos de la ventana
		"""
        self.descargando = 0
        self.conexion = 0

        self.lbip = tk.Label(self, text="IP")
        self.lbip.grid(row=0, column=0)

        self.txip = tk.Entry(self)
        self.txip.grid(row=0, column=1)

        self.lbport = tk.Label(self, text="PORT")
        self.lbport.grid(row=0, column=2)

        self.txport = tk.Entry(self)
        self.txport.grid(row=0, column=3)

        self.btconectar = tk.Button(self, text="Conectar", command=self.conectar)
        self.btconectar.grid(row=0, column=4)

        self.listBoxLista = tk.Listbox(self, selectmode="SINGLE")
        self.listBoxLista.grid(row=2,column=1, columnspan=2,  sticky=tk.W+tk.E)

        self.btdescargar = tk.Button(self, text="Descargar", command=self.descargarArchivo)
        self.btdescargar.grid(row = 2, column=3, sticky = tk.S)

        self.sdetener = tk.StringVar()
        self.sdetener.set("-")
        self.btdetener = tk.Button(self, textvariable=self.sdetener, command=self.detenerDescarga)
        self.btdetener.grid(row = 2, column=4, sticky = tk.S)

        self.sconexion = tk.StringVar()
        self.sconexion.set("No conectado")
        self.lbconexion = tk.Label(self,textvariable=self.sconexion)
        self.lbconexion.grid(row=3, column=3, columnspan = 2, sticky = tk.W+tk.E)

        self.s = tk.StringVar()
        self.lbporcentaje = tk.Label(self, textvariable=self.s)
        self.lbporcentaje.grid(row = 3, column=1, columnspan=2, sticky=tk.W+tk.E)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.grid(row=4, column=2)

    def conectar(self):
		"""
		Llama la funcion conectar del cliente. Inicia el estado de la conexion.
		"""
        conexion_con_servidor(self, self.txip.get(), int(self.txport.get()))
        self.mostrarConexion()
        thread_timeout=threading.Thread(target=self.timeoutCliente)
        thread_timeout.start()

    def actualizarLista(self, lista):
		"""
		Actualiza la lista de archivos.
		"""
        self.lista = lista
        self.listBoxLista.delete(0,tk.END)
        for l in self.lista:
            self.listBoxLista.insert(tk.END, l[1:-1])

    def descargarArchivo(self):
		"""
		Llama la funcion descargar del cliente. Inicia el estado "descargando"
		"""
        seleccionado = self.listBoxLista.get(self.listBoxLista.curselection())
        thread_archivo=threading.Thread(target=pedir_archivo, args=(self,seleccionado,))
        thread_archivo.start()
        self.detenerDescarga()

    def mostrarConexion(self):
		"""
		Cambia el estado de la conexion y lo muestra.
		"""
        if self.conexion:
            self.conexion = 0
            self.sconexion.set("Desconectado")
        else:
            self.conexion =  1
            self.sconexion.set("Conectado")

    def estaConectado(self):
		"""
		Retorna el estado de la conexion.
		"""
        return self.conexion

    def actualizarProgreso(self,progreso):
		"""
		Actualiza el porcentaje de progreso de la descarga.
		"""
        self.s.set('Progreso: {}%'.format(math.ceil(progreso)))

    def detenerDescarga(self):
		"""
		Detiene la descarga cambiando el estado y mostrandolo.
		"""
        if self.descargando:
            self.sdetener.set("Reanudar")
            self.descargando=0
        else:
            self.sdetener.set("Detener")
            self.descargando=1

    def estaDescargando(self):
		"""
		Retorna si se esta descargando actualmente o no.
		"""
        return self.descargando

    def timeoutCliente(self):
		"""
		Calcula cuando se debe terminar la sesion.
		"""
        while 1:
            time.sleep(5)
            if not self.descargando:
                self.mostrarConexion()
                root.destroy()
                return

if __name__ == '__main__':
	"""
	Si se llama este metodo, se crea la interfaz con la clase Application y se inicia
	"""
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
