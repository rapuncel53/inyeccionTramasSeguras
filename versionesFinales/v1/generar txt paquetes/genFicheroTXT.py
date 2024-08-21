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
        # tiempo de la captura
        # timestamp = packet.time

        # distribucion "normal" pero solo coger valores positivos
        # mu = 0.0006  # media en s
        # sigma = 0.001 # desviación estándar en s, ajusta según sea necesario
        # timestamp = -1
        # while timestamp <= 0:
        #     timestamp = ta + random.normalvariate(mu, sigma)

        # distribucion raileigh
        # sigma = 0.0005  # desviación estándar en s, ajusta según sea necesario
        # scale = sigma / np.sqrt(2 * (1 - (np.pi / 4)))
        # timestamp = ta + np.random.rayleigh(scale)

        # # distribucion raileigh con media
        media = 0.0006  # media en s
        scale=media/np.sqrt(np.pi/2)
        timestamp = ta + np.random.rayleigh(scale)



        timestamp = round(timestamp, 6)
        ta=timestamp
        #
        size = random.randint(80, 700)
        #la destination  un numero aleatorio del 1 al 3
        destination = random.randint(1,3)
        output_file.write(f"{timestamp} {size} {destination}\n")

    output_file.close()
    
read_pcap_file("captura.pcapng")