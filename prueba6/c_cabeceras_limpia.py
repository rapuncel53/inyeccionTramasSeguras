import struct
from a_preprocesado_limpia import leer_datos_paquetes
from b_ordenar_limpia import ordenarpaquetes

# Definición de los umbrales t1, t2, ..., t25
umbrales = [
    125, 141, 157, 173, 189, 205, 221, 237, 253, 269, 285,
    301, 317, 333, 349, 365, 381, 397, 413, 429, 445, 461,
    477, 493, 509
]

def colocarcabeceras(paquetes_ordenados):
    """
    Coloca cabeceras a los paquetes según su tamaño y una lista de umbrales.

    Argumentos:
    - paquetes_ordenados: diccionario donde las claves son direcciones MAC
      y los valores son los datos empaquetados correspondientes a esa MAC.

    Retorna:
    - Un diccionario donde las claves son direcciones MAC y los valores son 
      listas de paquetes con sus cabeceras.
    """
    paquetes_cabeceras = {}

    for mac, paquete in paquetes_ordenados.items():
        paquetes_cabeceras[mac] = []
        length = len(paquete)
        
        header_added = False
        
        for i, umbral in enumerate(umbrales):
            if length <= umbral:
                if i == 0:
                    paquetes_cabeceras[mac].append((b'\x80') + struct.pack('!H', 0) + paquete)
                else:
                    paquetes_cabeceras[mac].append((b'\x80') + struct.pack('!H', length - umbrales[0] + 1) + paquete[:umbrales[0]])
                    paquetes_cabeceras[mac].append((b'\x80') + paquete[umbrales[0]:])
                header_added = True
                break

        if not header_added:  # Para el caso de t25 y más allá
            paquetes_cabeceras[mac].append((b'\x80') + struct.pack('!H', length - umbrales[0] + 1) + paquete[:umbrales[0]])
            paquetes_cabeceras[mac].append((b'\x80') + paquete[umbrales[0]:])

    return paquetes_cabeceras

# Ejemplo de uso:
# eth_paquetes = leer_datos_paquetes("datosPaquetes.txt")
# for paquetes in eth_paquetes:
#     ord_paquetes = ordenarpaquetes(paquetes)
#     cab_paquetes = colocarcabeceras(ord_paquetes)
#     print(cab_paquetes)
