from scapy.all import Ether, IP, ICMP
from ordenarpaquetes import ordenarpaquetes

def CrearPaquetes():
    ethernet_packets = []
    dst_mac = ["11:11:11:11:11:11","11:11:11:11:11:11","11:11:11:11:11:11","22:22:22:22:22:22","22:22:22:22:22:22"]
    src_mac = ["00:00:00:00:00:00","00:00:00:00:00:00","00:00:00:00:00:00","00:00:00:00:00:00","00:00:00:00:00:00"]
    payloads = [IP(dst="8.8.8.8") / (b"A" * 100 ),IP(dst="7.7.7.7") / ICMP(),IP(dst="6.6.6.6") / ICMP(),IP(dst="5.5.5.5") / ICMP(),IP(dst="4.4.4.4") / ICMP()]

    # Verificar que las listas tengan la misma longitud
    if len(dst_mac) != len(src_mac) or len(dst_mac) != len(payloads):
        print("Las listas dest_mac, src_mac y payloads deben tener la misma longitud")
        return None
    
    # Crear los paquetes Ethernet
    for i in range(len(payloads)):
        ethernet_packet = Ether(dst=dst_mac[i], src=src_mac[i]) / payloads[i]
        ethernet_packets.append(ethernet_packet)
        print("Paquete Ethernet creado:")
        print(ethernet_packet.summary())
        ethernet_packet.show()
        print(ethernet_packet)
    
    
    return ethernet_packets

paquetes = CrearPaquetes()
for paquete in paquetes:
    print(paquete.dst)
    print(len(paquete.payload))
    print(paquete.payload)

paquetes_ordenados = ordenarpaquetes(paquetes)
print (paquetes_ordenados)
mac = list(paquetes_ordenados.keys())
print (mac[0])
