import os
import time
from scapy.all import Ether, IP
from escribir_archivo_eficiencias import escribir_en_archivo
import scapy.all as scapy
from scapy.layers.dot11 import Dot11, RadioTap

# Constantes de temporización y tasa de bits
Rb = 11 * 10**6
DIFS = 50 * 10**(-6)
Backoff_medio = 310 * 10**(-6)
TDataPreambulo = TAckPreambulo = 96 * 10**(-6)
SIFS = 10 * 10**(-6)
TAckMac = 14 * 8 / Rb

def calcular_tiempo_en_aire(tamano):
    """Calcula el tiempo en el aire de un paquete basado en su tamaño."""
    TDataMac = (tamano + 36) * 8 / Rb
    return DIFS + Backoff_medio + TDataPreambulo + TDataMac + SIFS + TAckPreambulo + TAckMac

def generar_paquete(tamano, destino):
    """Genera un paquete Ethernet basado en el tamaño y el destino."""
    if destino == '1':
        dst, ipdst = "11:11:11:11:11:11", "1.1.1.1"
    elif destino == '2':
        dst, ipdst = "22:22:22:22:22:22", "2.2.2.2"
    elif destino == '3':
        dst, ipdst = "33:33:33:33:33:33", "3.3.3.3"
    else:
        dst, ipdst = "00:00:00:00:00:00", "0.0.0.0"
        print("Destino no válido")

    # Generar payload con el tamaño especificado menos 20 bytes (cabecera IP)
    payload = b'\x11' * (tamano - 20)
    return Ether(dst=dst, src="00:00:00:00:00:00") / IP(dst=ipdst) / payload

def leer_datos_paquetes(nombre_archivo):
    """Lee los datos de los paquetes desde un archivo y los procesa."""
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            paquetes_leidos = []
            tiempoPaquete1 = None
            tamaño_destinos = {'1': 4, '2': 4, '3': 4}
            TTotal = 0
            primera_vez = True
            esperar_envio = 0

            for i, linea in enumerate(lineas):
                tiempo, tamano, destino = map(str.strip, linea.split(' '))
                tiempo = float(tiempo)
                tamano = int(tamano)
               

                # Asignar el tiempo inicial de referencia
                if primera_vez:
                    tiempo_inicial = time.time()
                    tiempo1 = tiempo
                    primera_vez = False

                if tiempoPaquete1 is None:
                    tiempoPaquete1 = tiempo

                if tamano < 600:
                    
                    

                    tamaño_destinos[destino] += (tamano + 2)

                    
                    #Print de tiempos

                    # print("time",time.time())
                    # print("tiempo inicial",tiempo_inicial)
                    # print("tiempo actual (time - inicial) ",time.time()-tiempo_inicial)
                    # print("tiempo paquete 1",tiempoPaquete1)
                    # print("tiempo1",tiempo1)
            
                    # print("tiempo paquete 1 (tiempo paquete 1 - tiempo 1)",tiempoPaquete1-tiempo1)
                    # print("tiempo fichero",tiempo)
                    # print("tiempo paquete actual (tiempo - tiempo1) ",tiempo-tiempo1)

                   
                    tamaño_total = sum(tamaño_destinos.values())
                    margen_tiempo = 0.1
                    # Condición para agrupar y devolver los paquetes leídos # 1448 pero no se porque desborda a veces aun siendo menor a 1500
                    if max(tamaño_destinos.values()) > 640 or tamaño_total > 1364 or (tiempo-tiempo1) - (tiempoPaquete1-tiempo1) > margen_tiempo:

                        #hay que esperar para enviarlo? 
                        if (tiempo-tiempo1) - (tiempoPaquete1-tiempo1) > 1:
                            esperar_envio= 1
                        tamaño_destinos[destino] -= (tamano + 2)

                        
                        

                        if paquetes_leidos:
                            if esperar_envio == 1:
                                while ((time.time()-tiempo_inicial) - (tiempoPaquete1-tiempo1))<1:
                                    time.sleep(0.000001)
                                esperar_envio = 0 
                                escribir_en_archivo(f"Tiempo total en el aire de los paquetes por separado = {TTotal} ,tiempo de envio agrupacion {tiempoPaquete1+margen_tiempo}")
                            else:
                                escribir_en_archivo(f"Tiempo total en el aire de los paquetes por separado = {TTotal} ,tiempo de envio agrupacion {tiempo}")
                            ##print(f"devuelvo los paquetes agrupados en {time.time()}")
                            #escribir_en_archivo(f"Tiempo total en el aire de los paquetes por separado = {TTotal}")
                            yield paquetes_leidos
                            tiempoPaquete1 = tiempo
                            paquetes_leidos = []
                            #print("-" * 85)
                            TTotal = 0
                            # Calcular el tiempo en el aire del paquete
                            Tpaquete = calcular_tiempo_en_aire(tamano)
                    
                            #escribir el paquete en el fichero de texto
                            ##print(f"paquete numero {i+1} Destino {destino} Taire {Tpaquete} Tamaño {tamano}")
                            escribir_en_archivo(f"paquete numero {i+1} Destino {destino} Taire {Tpaquete} Tamaño {tamano} Tiempo {tiempo}")
                            TTotal += Tpaquete
                        paquetes_leidos.append(generar_paquete(tamano, destino))
                        tamañodatos = tamano

                        tamaño_destinos = {'1': 4, '2': 4, '3': 4}
                        tamaño_destinos[destino] = tamano + 6
                    else:
                        # Calcular el tiempo en el aire del paquete
                        Tpaquete = calcular_tiempo_en_aire(tamano)
                    
                        #escribir el paquete en el fichero de texto
                        #print(f"paquete numero {i+1} Taire {Tpaquete} Tamaño {tamano}")
                        escribir_en_archivo(f"paquete numero {i+1} Destino {destino} Taire {Tpaquete} Tamaño {tamano} Tiempo {tiempo}")
                        TTotal += Tpaquete
                        paquetes_leidos.append(generar_paquete(tamano, destino))
                else:
                    Tpaquete = calcular_tiempo_en_aire(tamano+14)
                    #print(f"paquete individual numero {i+1} Taire {Tpaquete} Tamaño {tamano+14}")
                    escribir_en_archivo(f"paquete individual numero {i+1} Destino {destino} Taire {Tpaquete} Tamaño {tamano+14} Tiempo {tiempo}")

                    #enviar paquete aparte(FALTAN LAS VARIABLES)
                    packet = []
                    qoscontrol = b'\x00\x00'
                    IFACE = 'wlx00c0caa81a35'  # Interfaz de la tarjeta de red del transmisor
                    AP_MAC = '00:c0:ca:a8:1a:35'  # Dirección MAC del transmisor
                    AP_MAC_2 = '00:c0:ca:a4:73:7b'  # Dirección MAC del receptor
                    rates = 18  # Velocidad de transmisión por defecto (en 802.11b va de 1 Mbps a 11 Mbps)
                    datos = generar_paquete(tamano, destino)
                    # Construir el paquete a enviar
                    packet.append(RadioTap(present='Rate', Rate=int(rates)) / 
                    Dot11(type=2, subtype=8, addr1=AP_MAC_2, addr2=AP_MAC) / 
                    qoscontrol / datos)
                    # Enviar el paquete
                    scapy.sendp(packet, iface=IFACE, verbose=False)
                    
            # Devolver los paquetes restantes si quedan
            if paquetes_leidos:
                #print(f"tamaño de los datos a cifrar {sum(tamaño_destinos.values())}")
                #print(f"Tiempo total en el aire de los paquetes por separado = {TTotal}")
                escribir_en_archivo(f"Tiempo total en el aire de los paquetes por separado = {TTotal} ,tiempo de envio agrupacion {tiempo}")
                yield paquetes_leidos

    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
    except ValueError:
        print("Error al convertir el tiempo a entero.",ValueError)
