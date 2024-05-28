import os
import random
import time
from scapy.all import rdpcap,Ether,IP

Rb = 11
DIFS = 50 * 10**(-6)
Backoff_medio = 310 * 10**(-6)
TDataPreambulo = TAckPreambulo = 96 * 10**(-6)
#TDataMac = (L+36)*8/Rb
SIFS = 10 * 10**(-6)
TAckMac = 14*8/Rb
#Tpaquete = DIFS + Backoff_medio + TDataPreambulo +TDataMac + SIFS + TAckPreambulo + TAckMac


# Una funcion que lea un fichero de paquetes con tres columnas: tiempo de llegada, tamaño y estación destino.
def leer_datos_paquetes(nombre_archivo):
   
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines() #leemos las lineas del archivo
            # Inicializamos las variables
            paquetes = []
            tiempo_inicial = None
            tiempo_actual = time.time()
            tamañodatos = 0
            tamaño1 = 4
            tamaño2 = 4
            tamaño3 = 4
            paquetes_leidos = []
            i=0
            TTotal = 0

            for linea in lineas:
                
                # Dividir la línea en tiempo, tamaño y destino
                tiempo, tamano, destino = linea.strip().split(' ')
                tiempo = float(tiempo)
                tamano = int(tamano)
                
                
                #calcular tiempo en el aire
                L = int(tamano)
                TDataMac = (L+36)*8/Rb
                Tpaquete = DIFS + Backoff_medio + TDataPreambulo +TDataMac + SIFS + TAckPreambulo + TAckMac
                i += 1
                #print("paquete numero ",i," Taire ",Tpaquete," Tamaño ",tamano)
                TTotal += Tpaquete
                

                # Si el tiempo inicial no está asignado, asignarlo
                if tiempo_inicial is None:
                    tiempo_inicial = tiempo

                # Agregar el paquete actual a la lista de paquetes leídos
                if destino == '1':
                    tamaño1 += (tamano +2)
                    dst =  "11:11:11:11:11:11"
                    ipdst = "1.1.1.1"
                elif destino == '2':
                    tamaño2 += (tamano +2)
                    dst = "22:22:22:22:22:22"
                    ipdst = "2.2.2.2"
                elif destino == '3':
                    tamaño3 += (tamano +2)
                    dst = "33:33:33:33:33:33"
                    ipdst = "3.3.3.3"
                else:
                    dst = "00:00:00:00:00:00"
                    print ("Destino no válido")
                
                tamañodatos += tamano #acumulamos el tamaño de los paquetes
                

                

                # Si se cumple alguna de las condiciones, devolver los paquetes leídos
                tamañoT = tamaño1+tamaño2+tamaño3
                # print("tamaño1",tamaño1)
                # print("tamaño2",tamaño2)
                # print("tamaño3",tamaño3)
                # print("Tamaño Total",tamañoT)

                if tamaño1 > 640 or tamaño2 > 640 or tamaño3 > 640 or tamañoT > 1448 or tiempo - tiempo_inicial > 550:
                    
                    #nos guardamos el tamaño del ultimo paquete y ponemos el resto a cero
                    # print("tamaño de los datos utiles",tamañogrupo)
                    # print("tamaño1=",tamaño1,", tamaño2=",tamaño2,", tamaño3=",tamaño3)
                    #print("tiempo= ",(tiempo ))
                    # if tamaño1 > 600:
                    #     tamaño1 = tamano
                    #     tamaño2 = tamaño3 = 0
                    # elif tamaño2 > 600:
                    #     tamaño2 = tamano
                    #     tamaño1 = tamaño3 = 0
                    # elif tamaño3 > 600:
                    #     tamaño3 = tamano
                    #     tamaño2 = tamaño1 = 0
                    # elif tamañogrupo > 1300:
                    #     tamaño1 = tamaño2 =tamaño3 = 0
                    #tamañogrupo -= tamano #como el ultimo paquete que desborda los buffers no lo guardamos, lo tenemos que restar
                
                    tamañodatos -= tamano
                    if destino == '1':
                        tamaño1 -= (tamano +2)
                        print("tamaño de los datos utiles",tamañodatos)
                        print("tamaño1=",tamaño1,", tamaño2=",tamaño2,", tamaño3=",tamaño3)
                        print("tamaño de los datos a cifrar",tamaño1+tamaño2+tamaño3)
                        tamaño1 = tamaño2 = tamaño3 = 4
                        tamaño1 = (tamano +6)
                        
                    elif destino == '2':
                        tamaño2 -= (tamano +2)
                        print("tamaño de los datos utiles",tamañodatos)
                        print("tamaño1=",tamaño1,", tamaño2=",tamaño2,", tamaño3=",tamaño3)
                        print("tamaño de los datos a cifrar",tamaño1+tamaño2+tamaño3)
                        tamaño1 = tamaño2 = tamaño3 = 4
                        tamaño2 = (tamano +6)
                        
                    elif destino == '3':
                        tamaño3 -= (tamano +2)
                        print("tamaño de los datos utiles",tamañodatos)
                        print("tamaño1=",tamaño1,", tamaño2=",tamaño2,", tamaño3=",tamaño3)
                        print("tamaño de los datos a cifrar",tamaño1+tamaño2+tamaño3)
                        tamaño1 = tamaño2 = tamaño3 = 4
                        tamaño3 = (tamano +6)
                    
                    tamañodatos = tamano #pero lo guardamos para la siguiente iteracion
                    
                   
                    if paquetes_leidos:

                        yield paquetes_leidos  # Devolver los paquetes leídos hasta ahora (sin contar el actual)
                        paquetes_leidos = []  # Reiniciar la lista de paquetes leídos
                        
                        print("-------------------------------------------------------------------------------------")
                        print("Tiempo total en el aire de los paquetes por separado = ", TTotal)
                        i=TTotal = 0
                    tiempo_inicial = tiempo  # Actualizar el tiempo inicial

                #payload = os.urandom(tamano - 20)   #quitar cabecera IP
                #payload = b'\x11' * (tamano - 20)
                payload = b'\x99' * (tamano)
                #print("tamaño payload",len(payload))
                #ethernet_packet = Ether(dst=dst, src="00:00:00:00:00:00") / IP(dst=ipdst) / payload
                ethernet_packet = Ether(dst=dst, src="00:00:00:00:00:00") / payload
                #print("tamaño ethernet",len(ethernet_packet))
                
                paquetes_leidos.append(ethernet_packet) #ahora guardamos el paquete actual en los buffers (despues de enviarlos si se han llenado)
                #paquetes_leidos.append([tiempo, tamano, destino])

            # Devolver los paquetes restantes si quedan
            if paquetes_leidos:
                print("tamaño de los datos utiles",tamañodatos)
                print("tamaño de los datos a cifrar",tamaño1+tamaño2+tamaño3)
                print("tamaño1=",tamaño1,", tamaño2=",tamaño2,", tamaño3=",tamaño3)
                print("Tiempo total en el aire de los paquetes por separado = ", TTotal)
                i=TTotal=0
                print("-------------------------------------------------------------------------------------")
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