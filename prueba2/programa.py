import struct


def leer_datos_tramas(nombre_archivo):
    datos = []
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                # Dividir la línea en tamaño de trama y estación destino
                # Suponemos que están separados por un espacio o una coma
                tamaño, estacion = linea.strip().split()
                # Convertir el tamaño a entero si es necesario
                tamaño = int(tamaño)
                datos.append((tamaño, estacion))
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
    except ValueError:
        print("Error al convertir el tamaño de la trama a entero.")
    
    return datos

# Nombre del archivo a leer
nombre_archivo = 'datos_tramas.txt'

# Llamada a la función para leer los datos del archivo
datos_tramas = leer_datos_tramas(nombre_archivo)

# Imprimir los datos obtenidos
print("Tamaño de trama - Estación Destino")
for tamaño, estacion in datos_tramas:
    print(f"{tamaño} - {estacion}")


def ordenarpaquetes(paquetes,tamaño,destino):  #JUNTA LOS PAQUETES POR MAC DESTINO
    #ordenamos por macs destino
    macs = set() #coleccion de elementos unicos
    paquetes_ordenados = {}#diccionario
    for paquete,tamaño,destino in paquetes,tamaño,destino:
        if destino not in macs:                                     #para cada mac mira si es nueva
            macs.add(destino)                                       # Añadir la MAC a la lista de MACs conocidas
            paquetes_ordenados[destino] = []
        tamano = tamaño
        #print(tamano)
        longitud_empaquetada = struct.pack('!H', tamano) 
        print("longitud payload")
        print(longitud_empaquetada)
        print("payload")
        print(type(paquete.payload))
        len_paq = longitud_empaquetada+bytes(paquete.payload)
        paquetes_ordenados[paquete.dst].append(len_paq)     #apila en un array el tamaño y el payload
    for mac, paquetes in paquetes_ordenados.items():
        paquetes_ordenados[mac] = b''.join(paquetes)
    return paquetes_ordenados                                                                             #HAY QUE PONERLO EN UN FORMATO BUENO
        
    #para unirlos todos 
    #'11:11:11:11:11:11': ["b'007D'b'E\\x00\0078b'E\\x01\0078b'E\\x02"]
                           #hdr + paquete + hdr + paquete + ...   LO UNE EN PAYLOAD DE UN PAQUETE DE BYTES
   