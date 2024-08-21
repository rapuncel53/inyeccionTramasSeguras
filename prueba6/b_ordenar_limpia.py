import struct
from a_preprocesado_limpia import leer_datos_paquetes

def ordenarpaquetes(paquetes):  
    """
    Ordena paquetes de datos por la dirección MAC de destino y 
    empaqueta cada uno de ellos con su tamaño y contenido.

    Argumentos:
    - paquetes: lista de objetos de paquetes, cada uno con atributos 'dst' y 'payload'.

    Retorna:
    - Un diccionario donde las claves son direcciones MAC y los valores son 
      los datos empaquetados correspondientes a esa MAC.
    """

    macs = set()  # Conjunto para almacenar direcciones MAC únicas.
    paquetes_ordenados = {}  # Diccionario para almacenar los paquetes ordenados por MAC de destino.

    for paquete in paquetes:
        if paquete.dst not in macs:  # Si la MAC destino es nueva
            macs.add(paquete.dst)  # Añadir la MAC al conjunto de MACs conocidas
            paquetes_ordenados[paquete.dst] = []  # Crear una nueva entrada en el diccionario para esta MAC
        
        tamano = len(paquete.payload)  # Obtener el tamaño del payload
        longitud_empaquetada = struct.pack('!H', tamano)  # Empaquetar el tamaño como un entero sin signo de 2 bytes en formato de red (big-endian)
        
        # Concatenar el tamaño empaquetado con el payload del paquete
        len_paq = longitud_empaquetada + bytes(paquete.payload)
        
        # Añadir el paquete (tamaño + payload) a la lista correspondiente a la MAC destino en el diccionario
        paquetes_ordenados[paquete.dst].append(len_paq)
    
    # Unir todos los paquetes de cada MAC en un solo bloque de bytes
    for mac in paquetes_ordenados:
        paquetes_ordenados[mac] = b''.join(paquetes_ordenados[mac])

    return paquetes_ordenados  # Retornar el diccionario de paquetes ordenados y empaquetados

# Ejemplo de uso:
# eth_paquetes = leer_datos_paquetes("datosPaquetes.txt")
# for paquetes in eth_paquetes:
#     ord_paquetes = ordenarpaquetes(paquetes)
#     print(ord_paquetes)
