import os
import random
import sys
import time
from scapy.all import rdpcap,Ether,IP
from escribir_archivo_eficiencias import escribir_en_archivo
sys.path.append('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/versionesFinales/v1/calcular eficiencia')
from calculareficiencia2 import calculate_airtime

Rb = 11*10**6
DIFS = 50 * 10**(-6)
Backoff_medio = 310 * 10**(-6)
TDataPreambulo = TAckPreambulo = 96 * 10**(-6)
#TDataMac = (L+36)*8/Rb
SIFS = 10 * 10**(-6)
TAckMac = 14*8/Rb

#Tpaquete = DIFS + Backoff_medio + TDataPreambulo +TDataMac + SIFS + TAckPreambulo + TAckMac
# primera_vez_xd = 0
# tiempo1=0
# tiempo_inicial = None
# Una funcion que lea un fichero de paquetes con tres columnas: tiempo de llegada, tamaño y estación destino.

def leer_datos_paquetes():
    nombre_archivo = 'datosPaquetes2.txt'
    indi = 0
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines() #leemos las lineas del archivo
            # Inicializamos las variables
            paquetes = []
            tiempoPaquete1 = None
    
             
            tiempo_actual = time.time()
            tamañodatos = 0
            tamaño1 = 4
            tamaño2 = 4
            tamaño3 = 4
            paquetes_leidos = []
            i=0
            TTotal = 0
            primera_vez_xd = 0
            tiempo_inicial = None
            tiempo1=0

            for linea in lineas:


                
                # Dividir la línea en tiempo, tamaño y destino
                tiempo, tamano, destino = linea.strip().split(' ')
                tiempo = float(tiempo)
                tamano = int(tamano)
                

                #Asignar tiempos de referencia para los paquetes
                #print("primera vez",primera_vez_xd)
                if primera_vez_xd == 0:
                    primera_vez_xd = 1
                    #global tiempo_inicial
                    #print("tiempo primera vez",time.time() )
                    tiempo_inicial = time.time()
                    #print("tiempo inicial",tiempo_inicial)
                    #global tiempo1
                    tiempo1 = tiempo
                #tiempo_actual = time.time() 
                if tiempoPaquete1 == None:
                    tiempoPaquete1 = tiempo
                
                
                
                #calcular tiempo en el aire
                L = int(tamano)
                TDataMac = (L+36)*8/Rb
                Tpaquete = DIFS + Backoff_medio + TDataPreambulo +TDataMac + SIFS + TAckPreambulo + TAckMac
                Tpaquete2 = calculate_airtime("802.11b", 11* 10**6, L)
                print("Tiempo en el aire de la agrupacion = ",Tpaquete,Tpaquete2)
                i += 1
                print("paquete numero ",i," Taire ",Tpaquete," Tamaño ",tamano)
                escribir_en_archivo("paquete numero "+str(i)+" Destino "+destino+" Taire "+str(Tpaquete)+" Tamaño "+str(tamano))
                TTotal += Tpaquete
                

                

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
                tamañoT = tamaño1+tamaño2+tamaño3






                #Print de tiempos

                print("time",time.time())
                print("tiempo inicial",tiempo_inicial)
                print("tiempo actual (time - inicial) ",time.time()-tiempo_inicial)
                print("tiempo paquete 1",tiempoPaquete1)
                print("tiempo1",tiempo1)
        
                print("tiempo paquete 1 (tiempo paquete 1 - tiempo 1)",tiempoPaquete1-tiempo1)
                print("tiempo fichero",tiempo)
                print("tiempo paquete actual (tiempo - tiempo1) ",tiempo-tiempo1)

                # if ((tiempo-tiempo1) - (tiempoPaquete1-tiempo1))< 1:

                #     while ((time.time()-tiempo_inicial)<=(tiempo-tiempo1)):
                #         time.sleep(0.000001)
                # else:
                #     while ((time.time()-tiempo_inicial) - (tiempoPaquete1-tiempo1))<1:
                #         time.sleep(0.000001)


#1448 ttotal
                if tamaño1 > 640 or tamaño2 > 640 or tamaño3 > 640  or  tamañoT > 1300 or (tiempo-tiempo1) - (tiempoPaquete1-tiempo1) > 1: # segundos  epoch
                    
                    if (tiempo-tiempo1) - (tiempoPaquete1-tiempo1) > 1:
                        esperar_envio= 1
                    tamañodatos -= tamano
                    if destino == '1':
                        tamaño1 -= (tamano +2)
                        # print("tamaño de los datos utiles",tamañodatos)
                        # print("tamaño1=",tamaño1,", tamaño2=",tamaño2,", tamaño3=",tamaño3)
                        # print("tamaño de los datos a cifrar",tamaño1+tamaño2+tamaño3)
                        # print("Tiempo total en el aire de los paquetes por separado = ", TTotal)
                        tamaño1 = tamaño2 = tamaño3 = 4
                        tamaño1 = (tamano +6)
                        
                    elif destino == '2':
                        tamaño2 -= (tamano +2)
                        # print("tamaño de los datos utiles",tamañodatos)
                        # print("tamaño1=",tamaño1,", tamaño2=",tamaño2,", tamaño3=",tamaño3)
                        # print("tamaño de los datos a cifrar",tamaño1+tamaño2+tamaño3)
                        # print("Tiempo total en el aire de los paquetes por separado = ", TTotal)
                        tamaño1 = tamaño2 = tamaño3 = 4
                        tamaño2 = (tamano +6)
                        
                    elif destino == '3':
                        tamaño3 -= (tamano +2)
                        # print("tamaño de los datos utiles",tamañodatos)
                        # print("tamaño1=",tamaño1,", tamaño2=",tamaño2,", tamaño3=",tamaño3)
                        # print("tamaño de los datos a cifrar",tamaño1+tamaño2+tamaño3)
                        # print("Tiempo total en el aire de los paquetes por separado = ", TTotal)
                        tamaño1 = tamaño2 = tamaño3 = 4
                        tamaño3 = (tamano +6)
                    
                    tamañodatos = tamano #pero lo guardamos para la siguiente iteracion
                    
                   
                    if paquetes_leidos:
                        if esperar_envio == 1:
                            while ((time.time()-tiempo_inicial) - (tiempoPaquete1-tiempo1))<1:
                                time.sleep(0.000001)
                            esperar_envio = 0    
                        print("devuelvo los paquetes agrupados en ",time.time())
                        escribir_en_archivo("Tiempo total en el aire de los paquetes por separado = "+str(TTotal))
                        #packet_queue.put(paquetes_leidos) 
                        indi += 1
                        print("agrupacion numero ",indi)   
                        yield paquetes_leidos  # Devolver los paquetes leídos hasta ahora (sin contar el actual)
                        
                        tiempoPaquete1 = tiempo
                        paquetes_leidos = []  # Reiniciar la lista de paquetes leídos
                        
                        print("-------------------------------------------------------------------------------------")
                        
                        i=TTotal = 0
                    #tiempo_inicial = tiempo  # Actualizar el tiempo inicial

                #payload = os.urandom(tamano - 20)   #quitar cabecera IP
                payload = b'\x11' * (tamano - 20)
                #payload = b'\x99' * (tamano)
                #print("tamaño payload",len(payload))
                ethernet_packet = Ether(dst=dst, src="00:00:00:00:00:00") / IP(dst=ipdst) / payload
                #ethernet_packet = Ether(dst=dst, src="00:00:00:00:00:00") / payload
                #print("tamaño ethernet",len(ethernet_packet))
                
                paquetes_leidos.append(ethernet_packet) #ahora guardamos el paquete actual en los buffers (despues de enviarlos si se han llenado)
                #paquetes_leidos.append([tiempo, tamano, destino])

            # Devolver los paquetes restantes si quedan
            if paquetes_leidos:
                print("tamaño de los datos utiles",tamañodatos)
                print("tamaño de los datos a cifrar",tamaño1+tamaño2+tamaño3)
                print("tamaño1=",tamaño1,", tamaño2=",tamaño2,", tamaño3=",tamaño3)
                print("Tiempo total en el aire de los paquetes por separado = ", TTotal)
                escribir_en_archivo("Tiempo total en el aire de los paquetes por separado = "+str(TTotal))
                i=TTotal=0
                print("-------------------------------------------------------------------------------------")
                yield paquetes_leidos
                
        #packet_queue.put(None)         
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
    except ValueError:
        print("Error al convertir el tiempo a entero.")
    
    


# eth_paquetes = leer_datos_paquetes("datosPaquetes.txt")
# for paquetes in eth_paquetes:
#     print("paquetes")
#     print(paquetes)

#devuelve un array con los paquetes que va agrupando (cuando se cumple el tiempo o se llena el tamaño)