import tkinter as tk
from cliente_tcp import *
import threading
import math
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        #self.hi_there = tk.Button(self)
        #self.hi_there["text"] = "Hello World\n(click me)"
        #self.hi_there["command"] = self.say_hi
        #self.hi_there.pack(side="top")
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
        conexion_con_servidor(self, self.txip.get(), int(self.txport.get()))
        self.mostrarConexion()
        thread_timeout=threading.Thread(target=self.timeoutCliente)
        thread_timeout.start()

    def actualizarLista(self, lista):
        self.lista = lista
        self.listBoxLista.delete(0,tk.END)
        for l in self.lista:
            self.listBoxLista.insert(tk.END, l[1:-1])

    def descargarArchivo(self):
        seleccionado = self.listBoxLista.get(self.listBoxLista.curselection())
        thread_archivo=threading.Thread(target=pedir_archivo, args=(self,seleccionado,))
        thread_archivo.start()
        self.detenerDescarga()

    def mostrarConexion(self):
        if self.conexion:
            self.conexion = 0
            self.sconexion.set("Desconectado")
        else:
            self.conexion =  1
            self.sconexion.set("Conectado")

    def estaConectado(self):
        return self.conexion

    def actualizarProgreso(self,progreso):
        self.s.set('Progreso: {}%'.format(math.ceil(progreso)))

    def detenerDescarga(self):
        if self.descargando:
            self.sdetener.set("Reanudar")
            self.descargando=0
        else:
            self.sdetener.set("Detener")
            self.descargando=1

    def estaDescargando(self):
        return self.descargando

    def timeoutCliente(self):
        while 1:
            time.sleep(5)
            if not self.descargando:
                self.mostrarConexion()
                root.destroy()
                return

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
