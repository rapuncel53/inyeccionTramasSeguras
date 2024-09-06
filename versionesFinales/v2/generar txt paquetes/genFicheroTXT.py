import numpy as np
import random
from scapy.all import rdpcap

captura = "/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/versionesFinales/v2/generar txt paquetes/captura.pcapng"

#funcion que lee un pcap y devuelve un fichero con el tiempo de llegada del paquete, su tamaño y una estacion destino aleatoria
def read_pcap_file(file_path):
    output_file = open("datosPaqueteseeeeee.txt", "w")
    packets = rdpcap(file_path)
    ta=0
    

    for packet in packets:
        timestamp = packet.time
        size = len(packet)
        destination = random.randint(1,3)
        output_file.write(f"{timestamp} {size} {destination}\n")

    output_file.close()

#introducir la ruta del fichero pcap  
read_pcap_file(captura)