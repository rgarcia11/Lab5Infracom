import socket
import threading
import os.path
import time

##########################################################
# Datos importantes
##########################################################
#bind_ip = '0.0.0.0'
bind_ip = '127.0.0.1'
bind_port = 50005
TAM_BUFFER = 1024
MAX_THREADS = 100
threads = []
# Se crea el socket de espera y se conecta el servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((bind_ip, bind_port))
servidor.listen(5)

print ('Escuchando en (ip:puerto){}:{}'.format(bind_ip, bind_port))

##########################################################
# Se declaran los threads!
##########################################################

##### Esta funcion es un thread, maneja la transferencia de archivos con un cliente.
##### el cliente entra por parametro
def manejador_conexion(socket__conexion_servidor_cliente, nombre_cliente, puerto_cliente):
    #se envia la lista de archivos primero (sin los archivos de python!)
    lista_archivos = [a for a in os.listdir() if os.path.isfile(a)]
    #esta linea envia un string. Toca codificarlo a un stream de bytes.
    socket__conexion_servidor_cliente.sendto(str(lista_archivos).encode(), (nombre_cliente, puerto_cliente))

    #se recibe la peticion del archivo a enviar
    peticion = socket__conexion_servidor_cliente.recv(TAM_BUFFER)
    print ('Pidieron: {}'.format(peticion))
    #si la peticion no existe, espera una peticion correcta del cliente
    while not os.path.isfile(peticion):
        print('No existe!')
        socket__conexion_servidor_cliente.sendto('No existe'.encode(), (nombre_cliente, puerto_cliente))
        peticion = socket__conexion_servidor_cliente.recv(TAM_BUFFER)

    #se debe enviar el tamanho del archivo antes
    #con el tamanho el cliente puede ver progreso y transferir correctamente los archivos
    tam_archivo = os.path.getsize(peticion)
    print('El archivo pedido {} tiene tamanho {}'.format(peticion,tam_archivo))
    socket__conexion_servidor_cliente.sendto(str(tam_archivo).encode(), (nombre_cliente, puerto_cliente))
    #se abre el archivo que se quiere enviar, se lee en pedazos de tamanho TAM_BUFFER
    with open(peticion, 'rb') as f:
        archivo_enviar = f.read(TAM_BUFFER)
        #este while envia el archivo pedazo a pedazo hasta que ya no se lee mas.
        while archivo_enviar:
            socket__conexion_servidor_cliente.send(archivo_enviar)
            archivo_enviar = f.read(TAM_BUFFER)
    #se cierra el socket para escritura para prevenir errores raros
    socket__conexion_servidor_cliente.shutdown(socket.SHUT_WR)
    #se cierra el socket ahora si
    socket__conexion_servidor_cliente.close()
    print('Conexion cerrada con {}:{}'.format(nombre_cliente, puerto_cliente))

#####Esta funcion es un thread para la recepcion de clientes.
def manejador_clientes():
    #while True obligatorio para escuchar siempre
    while True:
        print('aceptando conexion!')
        #se acepta conexion y se crea el socket de la comunicacion
        socket__conexion_servidor_cliente, direccion = servidor.accept()
        nombre_cliente = direccion[0]
        puerto_cliente = direccion[1]
        print ('Se acepto una conexion desde {}:{}'.format(direccion[0], direccion[1]))
        ##Esto inicia el threading de la comunicacion para un solo cliente
        e = threading.Event()
        if len(threads) < MAX_THREADS:
            thread_cliente = threading.Thread(
                target=manejador_conexion,
                args=(socket__conexion_servidor_cliente, nombre_cliente, puerto_cliente,)  #con la coma!!
            )
            thread_cliente.start()
            threads.append(thread_cliente)
        #Se espera 15 segundos para ver actividad en el thread, o se cierra
        thread_cliente.join(15)
        if thread_cliente.is_alive():
            e.set()
        thread_cliente.join()


##########################################################
# Ahora si empieza el programa
##########################################################
#Se crea el thread para manejar clientes
thread_generador_clientes = threading.Thread(
    target=manejador_clientes
)
thread_generador_clientes.start()
#Se mantiene vivo un conteo de threads.
while True:
    print('Numero de threads activos: {}'.format(threading.activeCount()))
    time.sleep(3)
