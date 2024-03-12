from scapy.all import Ether, IP , ICMP , Raw
#from ordenarpaquetes import ordenarpaquetes, colocarcabeceras, paquetesacifrar

def CrearPaquetes():
    ethernet_packets = []
    dst_mac = ["11:11:11:11:11:11", "11:11:11:11:11:11", "11:11:11:11:11:11", "22:22:22:22:22:22", "22:22:22:22:22:22"]
    src_mac = ["00:00:00:00:00:00", "00:00:00:00:00:00", "00:00:00:00:00:00", "00:00:00:00:00:00", "00:00:00:00:00:00"]
    payloads = [IP(dst="8.8.8.8") / ICMP(), IP(dst="7.7.7.7") / ICMP(), IP(dst="6.6.6.6") / Raw(load= bytes.fromhex("FF" * 50)),
                IP(dst="5.5.5.5") / ICMP(), IP(dst="4.4.4.4") / ICMP()]

    # Verificar que las listas tengan la misma longitud
    if len(dst_mac) != len(src_mac) or len(dst_mac) != len(payloads):
        print("Las listas dest_mac, src_mac y payloads deben tener la misma longitud")
        return None

    # Crear los paquetes Ethernet
    for dst, src, payload in zip(dst_mac, src_mac, payloads):
        ethernet_packet = Ether(dst=dst, src=src) / payload
        ethernet_packets.append(ethernet_packet)
        # print("Paquete Ethernet creado:")
        # print(ethernet_packet.summary())
        # ethernet_packet.show()
        # print(ethernet_packet)

    return ethernet_packets
