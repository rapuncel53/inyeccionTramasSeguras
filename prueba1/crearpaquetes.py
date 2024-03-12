from scapy.all import Ether, IP, ICMP
from ordenarpaquetes import ordenarpaquetes, colocarcabeceras, paquetesacifrar

def CrearPaquetes():
    ethernet_packets = []
    dst_mac = ["11:11:11:11:11:11", "11:11:11:11:11:11", "11:11:11:11:11:11", "22:22:22:22:22:22", "22:22:22:22:22:22"]
    src_mac = ["00:00:00:00:00:00", "00:00:00:00:00:00", "00:00:00:00:00:00", "00:00:00:00:00:00", "00:00:00:00:00:00"]
    payloads = [IP(dst="8.8.8.8")/ ICMP(), IP(dst="7.7.7.7")/ ICMP(), IP(dst="6.6.6.6")/ ICMP()/b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11',
                IP(dst="5.5.5.5") , IP(dst="4.4.4.4") ]

    # Verificar que las listas tengan la misma longitud
    if len(dst_mac) != len(src_mac) or len(dst_mac) != len(payloads):
        print("Las listas dest_mac, src_mac y payloads deben tener la misma longitud")
        return None

    # Crear los paquetes Ethernet
    for dst, src, payload in zip(dst_mac, src_mac, payloads):
        ethernet_packet = Ether(dst=dst, src=src) / payload
        ethernet_packets.append(ethernet_packet)
        #print("Paquete Ethernet creado:")
        #print(ethernet_packet.summary())
        ethernet_packet.show()
        #print(ethernet_packet)

    return ethernet_packets

# paquetes = CrearPaquetes()

# for paquete in paquetes:
#     print(paquete.dst)
#     print(len(paquete.payload))
#     print(paquete.payload)

# paquetes_ordenados = ordenarpaquetes(paquetes)

# print("Paquetes ordenados:")
# print(paquetes_ordenados)

# #{'11:11:11:11:11:11': b'\x00\x14E\x00\x00\x14\x00\x01\x00\x00@\x001\x18\x9b\xd2\x9d\xef\x08\x08\x08\x08\x00\x1cE\x00\x00\x1c\x00\x01\x00\x00@\x013\x11\x9b\xd2\x9d\xef\x07\x07\x07\x07\x08\x00\xf7\xff\x00\x00\x00\x00\x00\x1cE\x00\x00\x1c\x00\x01\x00\x00@\x015\x13\x9b\xd2\x9d\xef\x06\x06\x06\x06\x08\x00\xf7\xff\x00\x00\x00\x00', '22:22:22:22:22:22': b'\x00\x1cE\x00\x00\x1c\x00\x01\x00\x00@\x017\x15\x9b\xd2\x9d\xef\x05\x05\x05\x05\x08\x00\xf7\xff\x00\x00\x00\x00\x00\x1cE\x00\x00\x1c\x00\x01\x00\x00@\x019\x17\x9b\xd2\x9d\xef\x04\x04\x04\x04\x08\x00\xf7\xff\x00\x00\x00\x00'}


# # Obtener la primera dirección MAC de los paquetes ordenados
# if paquetes_ordenados:
#     mac = list(paquetes_ordenados.keys())[0]
#     print("MAC:", mac)

# paquetes_con_cabeceras = colocarcabeceras(paquetes_ordenados)
# paquetes_a_cifrar = paquetesacifrar(paquetes_con_cabeceras)
# print("Paquetes a cifrar:")
# print(paquetes_a_cifrar)
