import struct
def ordenarpaquetes(paquetes):
    #ordenamos por macs destino
    macs = set() #coleccion de elementos unicos
    paquetes_ordenados = []#diccionario
    for paquete in paquetes:
        if paquete.dst not in macs:                                     #para cada mac mira si es nueva
            macs.add(paquete.dst)                                       # Añadir la MAC a la lista de MACs conocidas
            paquetes_ordenados.append = [paquete.dst,]
        tamano = len(paquete.payload) 
        print(tamano)
        longitud_empaquetada = struct.pack('!H', tamano) 
        #longitud_empaquetada = (7 + paquete.bit_length()) // 8 
        print("longitud")
        print(longitud_empaquetada)
        print("payload")
        print(type(paquete.payload))
        yepa = longitud_empaquetada+bytes(paquete.payload)
        paquetes_ordenados[paquete.dst].append(yepa)     #apila en un array el tamaño y el payload
    return paquetes_ordenados  