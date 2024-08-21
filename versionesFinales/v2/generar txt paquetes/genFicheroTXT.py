import numpy as np
import random
from scapy.all import rdpcap
#quiero un import para leer pcaps

#funcion que lee un pcap y devuelve un fichero con el tiempo de llegada del paquete, su tamaño y una estacion destino aleatoria
def read_pcap_file(file_path):
    output_file = open("datosPaquetes.txt", "w")
    packets = rdpcap(file_path)
    ta=0
    

    for packet in packets:
        timestamp = packet.time
        size = len(packet)
        destination = random.randint(1,3)
        output_file.write(f"{timestamp} {size} {destination}\n")

    output_file.close()
    
read_pcap_file("captura.pcapng")