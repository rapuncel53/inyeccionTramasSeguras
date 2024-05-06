

from scapy.all import *
#funcion que lee un pcap y devuelve un fichero con el tiempo de llegada del paquete, su tamaño y una estacion destino aleatoria
def read_pcap_file(file_path):
    output_file = open("output.txt", "w")
    packets = rdpcap(file_path)

    for packet in packets:
        timestamp = packet.time
        size = len(packet)
        #la destination  un numero aleatorio del 1 al 3
        destination = random.randint(1,3)
        output_file.write(f"{timestamp} {size} {destination}\n")

    output_file.close()



# Una funcion que lea un fichero de paquetes con tres columnas: tiempo de llegada, tamaño y estación destino.
def leer_datos_paquetes(nombre_archivo):
    datos = []
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                # Dividir la línea en tiempo de llegada, tamaño y estación destino
                # Suponemos que está separados por un espacio o una coma
                tiempo, tamano, estacion = linea.strip().split()
                # Convertir el tiempo a entero si es necesario
                tiempo = int(tiempo)
                datos.append((tiempo, tamano, estacion))
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
    except ValueError:
        print("Error al convertir el tiempo a entero.")
    
    return datos



