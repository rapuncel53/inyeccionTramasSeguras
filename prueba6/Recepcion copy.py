#!/usr/bin/env python

import socket
import time
import sys
import scapy.all as scapy
from scapy.all import IP, Ether, Raw
from scapy.layers.dot11 import Dot11, RadioTap
from scapy.sendrecv import sendp
from funciones_basicas import AMSDU_dec_limpia
from e_claves_limpia import claves

# Configuración inicial
IFACE2 = 'wlx00c0caa4737b'  # Interfaz de la tarjeta de red del receptor
AP_MAC_2 = '00:c0:ca:a4:73:7b'  # Dirección MAC del receptor
AP_MAC = '00:c0:ca:a8:1a:35'  # Dirección MAC del transmisor

key = b'\x01\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a'  # Clave de cifrado (ejemplo)
packet_count = 0

# Clave inicial (ejemplo)
Hdr = 2843796326746969865517775137331587486046904811886503323102856146256129856445998934622446266251760018784185737111736108364839797946641759100223128000616308091539303132799727619266259596828149083874517781740179944644935556803289876169647362898861310839047877703563616025850495911850867054594022211735083536843875628987627216327719706741910036986827677832845686557780528840150455730953809234694322995111692138428714417268185133762942049850455209445920069601946607745983683598930918306972219800721120122707225650964714727753960963676306745813930269021935324632162446815277154321124916795985950915416767654347652388677539

# Función para manejar los paquetes capturados
def PacketHandler(pkt):
    
    if pkt.haslayer(Dot11):
        dot11_layer = pkt.getlayer(Dot11)
        if pkt.type == 2 and pkt.subtype == 8 and pkt.addr1 == AP_MAC_2:
            paquetes_recuperados = []

            # Procesar paquete Dot11
            ver = pkt.getlayer(Dot11)
            numero = int.from_bytes(ver, byteorder='big')
            hexa = numero.to_bytes((numero.bit_length() + 7) // 8, byteorder='big')
            tiempo_actual = time.time()

            AMPDU_FINAL = b''
            for n, i in enumerate(hexa):
                if 26 <= n < len(hexa) - 4:
                    AMPDU_FINAL += i.to_bytes(1, byteorder='big') if i != 0 else b'\x00'

            intAMPDUfinal = int.from_bytes(AMPDU_FINAL, byteorder='big')

            global packet_count
            packet_count += 1
            ps, xs = claves("22:22:22:22:22:22", -1)
            MSDUs = AMSDU_dec_limpia(Hdr, intAMPDUfinal, [ps], [xs])
            paquetes_recibidos = None
            x = MSDUs[0].to_bytes((MSDUs[0].bit_length() + 7) // 8, byteorder='big')
            dst_ip = socket.inet_ntoa(x[21:25])

            if dst_ip == "2.2.2.2":
                paquetes_recibidos = x[3:]
                clave_siguiente = int(x[1:3].hex(), 16)
                ps, xs = claves("22:22:22:22:22:22", clave_siguiente)

                if clave_siguiente != 0:
                    MSDUs = AMSDU_dec_limpia(Hdr, intAMPDUfinal, [ps], [xs])
                    x = MSDUs[0].to_bytes((MSDUs[0].bit_length() + 7) // 8, byteorder='big')
                    paquetes_recibidos += x[1:]

            if paquetes_recibidos:
                tam = 0
                while len(paquetes_recibidos) > tam:
                    tamaño_siguiente = int(paquetes_recibidos[tam:tam+2].hex(), 16)
                    paquetes_recuperados.append(b'\x00\x00\x00\x00\x00\x00\x16\x16\x16\x16\x16\x16\x9b\xd2' + paquetes_recibidos[tam+2:tam+2+tamaño_siguiente])
                    tam += tamaño_siguiente + 2

            

            # Guardar los paquetes en un archivo pcap
            packets = [Raw(load=byte_packet) for byte_packet in paquetes_recuperados]
            for packet in packets:
                packet.time = tiempo_actual
            scapy.wrpcap('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba6/paquetes_recuperados.pcap', packets, append=True)

# Inicializar archivo pcap
scapy.wrpcap('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba6/paquetes_recuperados.pcap', [])

# Iniciar la captura de paquetes
scapy.sniff(iface=IFACE2, prn=PacketHandler, timeout=30000)
