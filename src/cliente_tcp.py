import socket
import threading
import time
import os
import interfaz_cliente_tcp
import sys
"""
Script de conexion con el servidor y transferencia de archivos
"""

TAM_BUFFER = 5120
lista_archivos = []
dir_src = os.getcwd()
dir_descargas = os.path.join(dir_src[:-(len(os.sep)+len("src"))],"descargas")
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def cerrarConexion(interfaz):
    """
    Termina la conexion
    """
    try:
        cliente.sendto(b'TERMINADA',(nombre_servidor, puerto_servidor))
        cliente.shutdown(socket.SHUT_WR)
        cliente.close()
    except:
        print('No hay conexion')

def conexion_con_servidor(interfaz, nombre_servidor0, puerto_servidor0):
    """
    Maneja la conexion con el servidor. Lanzara error si no lo logra.
    """
    global lista_archivos
    global estado_conexion
    global inicio_descarga
    global nombre_servidor
    global puerto_servidor

    nombre_servidor = nombre_servidor0
    puerto_servidor = puerto_servidor0

    print('Intentare conectarme a {}:{}'.format(nombre_servidor, puerto_servidor))
    cliente.connect((nombre_servidor, puerto_servidor))
    print('conectado')

    #Recibir e imprimir la lista de archivos
    lista_archivos = str(cliente.recv(TAM_BUFFER))
    if lista_archivos == b'Intente mas tarde':
        interfaz.mensajeEmergente('No se pudo establecer conexion.')
        cerrarConexion(interfaz)
        return

    lista_archivos = lista_archivos[3:-2].split(", ")
    interfaz.actualizarLista(lista_archivos)


def pedir_archivo(interfaz, mensaje):
    """
    Se encarga de pedir un archivo y descargarlo.
    """
    print('Pedi {}'.format(mensaje))
    cliente.sendto(mensaje.encode(),(nombre_servidor, puerto_servidor))
    print('Mensaje enviado')
    tam_archivo = cliente.recv(TAM_BUFFER)
    print(tam_archivo)
    if not tam_archivo == b'No existe':
        tam_archivo = int(tam_archivo)
        print('Tam archivo: {}'.format(tam_archivo))
        tam_actual = 0
        buff = b""
        print('Recibiendo:')
        num_archivos = 0
        os.chdir(dir_descargas)
        with open(mensaje, 'wb') as f:
            while tam_actual < tam_archivo:
                if not interfaz.estaConectado():
                    cliente.close()
                    return

                if interfaz.estaDescargando():
                    progreso = tam_actual/tam_archivo*100

                    archivo_recibir = cliente.recv(TAM_BUFFER)
                    num_archivos+=1
                    if not archivo_recibir:
                        break
                    if len(archivo_recibir) + tam_actual > tam_archivo:
                        archivo_recibir = archivo_recibir[:tam_archivo-tam_actual]
                    buff += archivo_recibir
                    tam_actual += len(archivo_recibir)
                    f.write(archivo_recibir)
                    interfaz.actualizarProgreso(progreso)
        tiempo_final = time.time()
        cliente.sendto(str(tiempo_final).encode(),(nombre_servidor, puerto_servidor))
        tiempo_transcurrido = str(cliente.recv(TAM_BUFFER).decode())
        tam_diferencia = tam_archivo - tam_actual
        if tam_diferencia == 0:
            stiempo = 'Recibido archivo completo. Tiempo transcurrido: {}. Bytes esperados: {}. Bytes recibidos: {}. Paquetes recibidos: {}'.format(tiempo_transcurrido,tam_archivo,tam_actual,num_archivos)
            print(stiempo)
            interfaz.mensajeEmergente(stiempo)
        else:
            stiempo = 'Recibido archivo incompleto. Tiempo transcurrido: {}. Bytes esperados: {}. Bytes recibidos: {}. Paquetes recibidos: {}'.format(tiempo_transcurrido,tam_archivo,tam_actual,num_archivos)
            print(stiempo)
            interfaz.mensajeEmergente(stiempo)
        interfaz.finalizarDescarga()

def timeoutCliente(interfaz):
    """
    Calcula cuando se debe terminar la sesion.
    """
    while 1:
        time.sleep(30)
        if not interfaz.descargando:
            interfaz.mostrarConexion()
            interfaz.terminar()
            return



if __name__ == '__main__':
    """
    Si se corre el programa, las interacciones son por consola.
    """
    print('inicio!')
    nombre_servidor = input('Digite IP del servidor (Azure: 52.234.215.61. Local: 127.0.0.1): ')
    puerto_servidor = int(input('Digite puerto del servidor (5005): '))
    conexion_con_servidor()
