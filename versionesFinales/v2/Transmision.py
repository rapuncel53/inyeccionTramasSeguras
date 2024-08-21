# -*- coding: utf-8 -*-
import os
import time
import scapy.all as scapy
import sys

# Añadir ruta para importar módulos personalizados
sys.path.append('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba3/calcular eficiencia')
sys.path.append('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba6/datosPaquetes')
from scapy.layers.dot11 import Dot11, RadioTap
from scapy.layers.inet import UDP
from scapy.packet import Raw
from a_preprocesado_limpia import leer_datos_paquetes
from b_ordenar_limpia import ordenarpaquetes
from c_cabeceras_limpia import colocarcabeceras
from d_acifrar_limpia import paquetesacifrar
from funciones_basicas import cifrarCRTbasica
from calculareficiencia2 import calculate_airtime
from escribir_archivo_eficiencias import escribir_en_archivo

# Configuración inicial
ap_list = []  # Lista de índices para controlar los paquetes recibidos
IFACE = 'wlx00c0caa81a35'  # Interfaz de la tarjeta de red del transmisor
AP_MAC = '00:c0:ca:a8:1a:35'  # Dirección MAC del transmisor
AP_MAC_2 = '00:c0:ca:a4:73:7b'  # Dirección MAC del receptor
rates = 18  # Velocidad de transmisión por defecto (en 802.11b va de 1 Mbps a 11 Mbps)

# Constantes de temporización y tasa de bits
Rb = 11 * 10**6  # Tasa de bits (11 Mbps)
DIFS = 50 * 10**(-6)  # Tiempo DIFS
Backoff_medio = 310 * 10**(-6)  # Tiempo medio de backoff
TDataPreambulo = TAckPreambulo = 96 * 10**(-6)  # Tiempo de preámbulo
SIFS = 10 * 10**(-6)  # Tiempo SIFS
TAckMac = 14 * 8 / Rb  # Tiempo de ACK MAC

# Clave de cifrado (ejemplo)
key = b'\x01\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a'

ind = 0  # Índice para controlar el número de paquetes enviados

# Función para manejar el envío de paquetes
def PacketHandler(paquetes, ps, xs, Hdr):
    packet = []
    qoscontrol = b'\x00\x00'
    
    # Cifrar el paquete
    #print("paquetes",paquetes, "ps", ps, "xs", xs, "Hdr", Hdr)

    mpduCi = cifrarCRTbasica(paquetes, ps, xs, Hdr)
    #print("mpduCi", mpduCi)
    # Construir el paquete a enviar
    packet.append(RadioTap(present='Rate', Rate=int(rates)) / 
    Dot11(type=2, subtype=8, addr1=AP_MAC_2, addr2=AP_MAC, addr3=AP_MAC) / 
    qoscontrol / mpduCi)
    
    print("Longitud de mpduCi:", len(mpduCi))
    print("Enviando paquete en:", time.time())
    
    # Enviar el paquete
    scapy.sendp(packet, iface=IFACE, verbose=False)

# Función para calcular el tiempo en el aire de un paquete
def calcular_tiempo_en_aire(tamano):
    TDataMac = (tamano + 36) * 8 / Rb
    return DIFS + Backoff_medio + TDataPreambulo + TDataMac + SIFS + TAckPreambulo + TAckMac

# Función principal
def main():
    dir = os.getcwd()
    tipoPaquetes = "/datosPaquetes/50_200/datosPaquetes50_200_80.txt"
    eth_paquetes = leer_datos_paquetes(dir + tipoPaquetes)
    print("datosPaquetes :",tipoPaquetes)
    global ind
    
    for paquetes in eth_paquetes:
        # Ordenar y preparar los paquetes
        ord_paquetes = ordenarpaquetes(paquetes)
        cab_paquetes = colocarcabeceras(ord_paquetes)
        cif_paquetes = paquetesacifrar(cab_paquetes)
        
        # Calcular el tamaño total a cifrar
        tamañocifrar = sum(len(paquete) for paquete in cif_paquetes[0])
        ##print("Tamaño total a cifrar:", tamañocifrar)
        
        # Calcular el tiempo en el aire de los paquetes
        Tpaquete = calcular_tiempo_en_aire(tamañocifrar)
        #Tpaquete2 = calculate_airtime("802.11b", 11 * 10**6, tamañocifrar)
        ##print("Tiempo en el aire de la agrupación (calculado manualmente):", Tpaquete)
        ##print("Tiempo en el aire de la agrupación (calculado con función):", Tpaquete2)
        escribir_en_archivo("Tiempo en el aire de la agrupación (calculado con función): " + str(Tpaquete))
        
        # Manejar y enviar los paquetes cifrados
        Total = sum(len(paquete) for paquete in cif_paquetes[0])
        ##print("Tamaño TOTAL:", Total)
        ind += 1
        ##print("Número de paquete:", ind)
        PacketHandler(cif_paquetes[0], cif_paquetes[1], cif_paquetes[2], cif_paquetes[3])

if __name__ == "__main__":
    main()
