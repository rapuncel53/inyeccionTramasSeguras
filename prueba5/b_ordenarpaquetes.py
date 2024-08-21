import struct
from a_generarFicheroPaquetes import leer_datos_paquetes


def ordenarpaquetes(paquetes):  #JUNTA LOS PAQUETES POR MAC DESTINO
    #ordenamos por macs destino
    macs = set() #coleccion de elementos unicos
    paquetes_ordenados = {}#diccionario
    for paquete in paquetes:
        if paquete.dst not in macs:                                     #para cada mac mira si es nueva
            macs.add(paquete.dst)                                       # Añadir la MAC a la lista de MACs conocidas
            paquetes_ordenados[paquete.dst] = []
        tamano = len(paquete.payload) 
        #print(tamano)
        longitud_empaquetada = struct.pack('!H', tamano) 
        # print("longitud payload")
        # print(longitud_empaquetada)
        # print("payload")
        # print(type(paquete.payload))
        len_paq = longitud_empaquetada+bytes(paquete.payload)
        paquetes_ordenados[paquete.dst].append(len_paq)     #apila en un array el tamaño y el payload
    for mac, paquetes in paquetes_ordenados.items():
        paquetes_ordenados[mac] = b''.join(paquetes)
    return paquetes_ordenados 

# eth_paquetes = leer_datos_paquetes("datosPaquetes.txt")
# for paquetes in eth_paquetes:
#     ord_paquetes = ordenarpaquetes(paquetes)
#     print(ord_paquetes)

  