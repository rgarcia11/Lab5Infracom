import socket
import threading
import tkinter
import time
import os
import interfaz_cliente_tcp
############################################################
#             COMUNICACION CON EL SERVIDOR!
############################################################


TAM_BUFFER = 5120
lista_archivos = []
estado_conexion = 0
inicio_descarga = 0
dir_src = os.getcwd()
dir_descargas = os.path.join(dir_src[:-(len(os.sep)+len("src"))],"descargas")
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#nombre_servidor = '52.234.215.61'
#nombre_servidor = '127.0.0.1'

#Maneja la conexion con el servidor
def conexion_con_servidor(interfaz, nombre_servidor0, puerto_servidor0):
    global lista_archivos
    global estado_conexion
    global inicio_descarga
    global nombre_servidor
    global puerto_servidor

    nombre_servidor = nombre_servidor0
    puerto_servidor = puerto_servidor0


    #Termina la conexion
    print('Intentare conectarme a {}:{}'.format(nombre_servidor, puerto_servidor))
    cliente.connect((nombre_servidor, puerto_servidor))
    print('conectado')
    estado_conexion = 1

    #Recibir e imprimir la lista de archivos
    lista_archivos = str(cliente.recv(TAM_BUFFER))
    if lista_archivos == b'Intente mas tarde':
        cliente.close()
        return

    lista_archivos = lista_archivos[3:-2].split(", ")
    interfaz.actualizarLista(lista_archivos)
    #print(a for a in lista_archivos)
    #for a in lista_archivos:
        #print(a)
    #print(type(lista_archivos))
    #print(lista_archivos)

    #Se inicia el proceso de timeout para que no demore mas de 15 s en escoger
    #thread_timeout=threading.Thread(
    #    target=timeout_cliente
    #)
    #thread_timeout.start()

    #Se inicia el proceso de pedir un archivo!
    #thread_archivo=threading.Thread(
    #    target=pedir_archivo
    #)
    #thread_archivo.start()

#peticion del archivo
def pedir_archivo(interfaz, mensaje):
    #mensaje = input('Ingrese el nombre del archivo a descargar, o deje vacio para terminar: ')
    #Este while es para tener comunicacion mientras no escriba vacio

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
        inicio_descarga = 1
        num_archivos = 0
        os.chdir(dir_descargas)
        with open(mensaje, 'wb') as f:
            while tam_actual < tam_archivo:
                #print('Tamanho actual del archivo: {}'.format(tam_actual))
                #print('Tamanho del archivo: {}'.format(tam_archivo))
                #if not interfaz.estaConectado():
                    #print('debo moril')
                if not interfaz.estaConectado():
                    cliente.close()
                    return

                if interfaz.estaDescargando():
                    progreso = tam_actual/tam_archivo*100

                    #print('Recibiendo... {0:.1f}%'.format(progreso))

                    archivo_recibir = cliente.recv(TAM_BUFFER)
                    num_archivos+=1
                    if not archivo_recibir:
                        break
                    if len(archivo_recibir) + tam_actual > tam_archivo:
                        archivo_recibir = archivo_recibir[:tam_archivo-tam_actual]
                    buff += archivo_recibir
                    tam_actual += len(archivo_recibir)
                    #print('chunk: {}'.format(archivo_recibir))
                    f.write(archivo_recibir)
                    interfaz.actualizarProgreso(progreso)
        tiempo_final = time.time()
        cliente.sendto(str(tiempo_final).encode(),(nombre_servidor, puerto_servidor))
        tiempo_transcurrido = str(cliente.recv(TAM_BUFFER).decode())
        #print('Archivo: {}'.format(archivo_recibir))
        tam_diferencia = tam_archivo - tam_actual
        if tam_diferencia == 0:
            print('Recibido archivo completo. Tiempo transcurrido: {}. Bytes esperados: {}. Bytes recibidos: {}. Paquetes recibidos: {}'.format(tiempo_transcurrido,tam_archivo,tam_actual,num_archivos))
        else:
            print('Recibido archivo incompleto. Tiempo transcurrido: {}. Bytes esperados: {}. Bytes recibidos: {}. Paquetes recibidos: {}'.format(tiempo_transcurrido,tam_archivo,tam_actual,num_archivos))
        inicio_descarga = 0
        interfaz.detenerDescarga()
        cliente.close()

if __name__ == '__main__':
    print('inicio!')
    nombre_servidor = input('Digite IP del servidor (Azure: 52.234.215.61. Local: 127.0.0.1): ')
    puerto_servidor = int(input('Digite puerto del servidor (5005): '))
    conexion_con_servidor()
