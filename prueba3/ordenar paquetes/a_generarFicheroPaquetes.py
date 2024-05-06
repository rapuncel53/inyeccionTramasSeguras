import os
import random
import time
from scapy.all import rdpcap,Ether,IP



# Una funcion que lea un fichero de paquetes con tres columnas: tiempo de llegada, tamaño y estación destino.
def leer_datos_paquetes(nombre_archivo):
   
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines() #leemos las lineas del archivo
            # Inicializamos las variables
            paquetes = []
            tiempo_inicial = None
            tiempo_actual = time.time()
            tamañogrupo = 0
            tamaño1 = 0
            tamaño2 = 0
            tamaño3 = 0
            paquetes_leidos = []

            for linea in lineas:
                # Dividir la línea en tiempo, tamaño y destino
                tiempo, tamano, destino = linea.strip().split(' ')
                tiempo = float(tiempo)
                tamano = int(tamano)
                

                # Si el tiempo inicial no está asignado, asignarlo
                if tiempo_inicial is None:
                    tiempo_inicial = tiempo

                # Agregar el paquete actual a la lista de paquetes leídos
                if destino == '1':
                    tamaño1 += tamano
                    dst =  "11:11:11:11:11:11"
                    ipdst = "1.1.1.1"
                elif destino == '2':
                    tamaño2 += tamano
                    dst = "22:22:22:22:22:22"
                    ipdst = "2.2.2.2"
                elif destino == '3':
                    tamaño3 += tamano
                    dst = "33:33:33:33:33:33"
                    ipdst = "3.3.3.3"
                else:
                    dst = "00:00:00:00:00:00"
                    print ("Destino no válido")
                
                # Si se cumple alguna de las condiciones, devolver los paquetes leídos
                if tamaño1 > 600 or tamaño2 > 600 or tamaño3 > 600 or tiempo - tiempo_inicial > 5:
                    
                    #nos guardamos el tamaño del ultimo paquete y ponemos el resto a cero
                    print("tamaño de los datos utiles",tamañogrupo)
                    if tamaño1 > 600:
                        tamaño1 = tamano
                        tamaño2 = tamaño3 = 0
                    elif tamaño2 > 600:
                        tamaño2 = tamano
                        tamaño1 = tamaño3 = 0
                    elif tamaño3 > 600:
                        tamaño3 = tamano
                        tamaño2 = tamaño1 = 0
                    if paquetes_leidos:
                        tamañogrupo = 0
                        yield paquetes_leidos  # Devolver los paquetes leídos hasta ahora (sin contar el actual)
                        paquetes_leidos = []  # Reiniciar la lista de paquetes leídos
                    tiempo_inicial = tiempo  # Actualizar el tiempo inicial

                payload = os.urandom(tamano - 20)   #quitar cabecera IP
                #print("tamaño payload",len(payload))
                ethernet_packet = Ether(dst=dst, src="00:00:00:00:00:00") / IP(dst=ipdst) / payload
                #print("tamaño ethernet",len(ethernet_packet))
                tamañogrupo += tamano #acumulamos el tamaño de los paquetes
                paquetes_leidos.append(ethernet_packet)
                #paquetes_leidos.append([tiempo, tamano, destino])

            # Devolver los paquetes restantes si quedan
            if paquetes_leidos:
                print("tamaño de los datos utiles",tamañogrupo)
                yield paquetes_leidos
                
                
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
    except ValueError:
        print("Error al convertir el tiempo a entero.")
    
    


# eth_paquetes = leer_datos_paquetes("datosPaquetes.txt")
# for paquetes in eth_paquetes:
#     print("paquetes")
#     print(paquetes)

#devuelve un array con los paquetes que va agrupando (cuando se cumple el tiempo o se llena el tamaño)