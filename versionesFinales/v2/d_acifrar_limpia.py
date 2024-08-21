from e_claves_limpia import *

from a_preprocesado_limpia import leer_datos_paquetes
from b_ordenar_limpia import ordenarpaquetes
from c_cabeceras_limpia import colocarcabeceras

# Constante para la cabecera Hdr
HDR = 2843796326746969865517775137331587486046904811886503323102856146256129856445998934622446266251760018784185737111736108364839797946641759100223128000616308091539303132799727619266259596828149083874517781740179944644935556803289876169647362898861310839047877703563616025850495911850867054594022211735083536843875628987627216327719706741910036986827677832845686557780528840150455730953809234694322995111692138428714417268185133762942049850455209445920069601946607745983683598930918306972219800721120122707225650964714727753960963676306745813930269021935324632162446815277154321124916795985950915416767654347652388677539

def paquetesacifrar(paquetes_con_cabeceras):  
    """
    Asigna las claves a cada paquete y devuelve los paquetes a cifrar junto con sus claves.

    Argumentos:
    - paquetes_con_cabeceras: diccionario donde las claves son direcciones MAC
      y los valores son listas de paquetes con cabeceras.

    Retorna:
    - Una lista de paquetes a cifrar.
    - Listas de claves ps y xs correspondientes.
    - La constante Hdr.
    """
    paquetes_a_cifrar = []
    xs = []
    ps = []

    for mac, paquetes in paquetes_con_cabeceras.items():
        primer_llamado = True  # Bandera para controlar la primera llamada

        for paquete in paquetes:
            paquetes_a_cifrar.append(paquete)
            if primer_llamado:
                ps1, xs1 = claves(mac, -1)
                ps.append(ps1)
                xs.append(xs1)
                primer_llamado = False
            else:
                ps2, xs2 = claves(mac, len(paquete))
                ps.append(ps2)
                xs.append(xs2)

    return paquetes_a_cifrar, ps, xs, HDR

# Ejemplo de uso:
# eth_paquetes = leer_datos_paquetes("datosPaquetes.txt")
# for paquetes in eth_paquetes:
#     ord_paquetes = ordenarpaquetes(paquetes)
#     cab_paquetes = colocarcabeceras(ord_paquetes)
#     cif_paquetes, ps, xs, hdr = paquetesacifrar(cab_paquetes)
#     tamañocifrar = sum(len(paquete) for paquete in cif_paquetes)
#     print("tamaño total a cifrar", tamañocifrar)
