from crearpaquetes import *
from ordenarpaquetes import *


paquetes = CrearPaquetes()

for paquete in paquetes:
    print(paquete)
    print(paquete.dst)
    print(len(paquete.payload))
    print(paquete[Ether].payload)
    
paquetes_ordenados = ordenarpaquetes(paquetes)

# print("Paquetes ordenados:")
# print(paquetes_ordenados)

# # Obtener la primera dirección MAC de los paquetes ordenados
# if paquetes_ordenados:
#     mac = list(paquetes_ordenados.keys())[0]
#     print("MAC:", mac)

# paquetes_con_cabeceras = colocarcabeceras(paquetes_ordenados)
# paquetes_a_cifrar = paquetesacifrar(paquetes_con_cabeceras)
# print("Paquetes a cifrar:")
# print(paquetes_a_cifrar)

