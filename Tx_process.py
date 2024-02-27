# -*- coding: utf-8 -*-
import scapy.all as scapy
import sys
from scapy.layers.dot11 import *
from scapy.layers.dot11 import Dot11, LLC, RadioTap, Dot11Beacon, Dot11Elt, Dot11ProbeResp
from scapy.layers.inet import UDP
from scapy.packet import Raw
from scapy.utils import hexdump, checksum
from datos import *
import pickle5 as pickle

ap_list = []                                #Lista de indices para controlar que paquetes nos han llegado
IFACE = 'wlx00c0caa81a35'                   #Interfaz de la targeta de red del transmisor
AP_MAC = '00:c0:ca:a8:1a:36'               #Direccion mac del transmisor
AP_MAC_2= '00:c0:ca:a4:73:7b'               #Direccion mac del receptor()
rates=0                                      #Velocidad de transmision
forma=0
#key = secrets.token_bytes(16)  # Aquí debería coger una clave asociada al receptor
key = b'\x01\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a'



def PacketHandler(pkt):
    # Capturamos el Assoc request
    if pkt.subtype == 0 :
        if pkt.subtype not in ap_list:
            infoPacket = pkt.getlayer(Dot11Elt)
            if infoPacket.info.decode()=="apjulian":
                ap_list.append(pkt.subtype)
                packet=[]
                packet.append(RadioTap(present='Rate',Rate=int(rates)) / Dot11(subtype=1, addr1=pkt.addr2, addr2=AP_MAC, addr3=AP_MAC) / Dot11AssoResp(cap="ESS+CFP") /
                               Dot11Elt(ID='SSID', info=infoPacket.info.decode()) / Dot11Elt(ID='Supported Rates',
                                                                          info="\x82\x84\x8b\x0c\x12\x96\x18\x24") /
                               Dot11Elt(ID='DSSS Set', info=chr(56)) / Dot11EltHTCapabilities(SM_Power_Save=3,
                                                                                              Short_GI_20Mhz=1, Tx_STBC=1,
                                                                                              Rx_STBC=1, Max_A_MSDU=1,
                                                                                              DSSS_CCK=1)
                               / Dot11Elt(ID='Extended Supported Rates', info="\xb0\x48\x60\x6c"))
                sendp(packet, iface=IFACE, verbose=False)
                print("Enviado Association response")
                # Paquete ADDBA Request
                packet = []
                data = "\x03\x00\x01\x00\x10\x00\x00\x03\x0a"
                data2 = "\x00\x03\x61\x70\x30"
                packet.append(RadioTap(present='Rate',Rate=int(rates)) / Dot11(subtype=13, addr1=pkt.addr2, addr2=AP_MAC, addr3=AP_MAC) / data / Dot11Elt(ID='SSID', info=infoPacket.info.decode()))
                sendp(packet, iface=IFACE, verbose=False)
                print("Enviado correctamente ADDBA Request..")

    #Capturamos el ADDBA Response
    if pkt.type==0 and pkt.subtype == 13:
        if pkt.subtype not in ap_list:
            if pkt.addr2==AP_MAC_2:
                ap_list.append(pkt.subtype)
                # Paquete AMPDU SIMPLE
                print("Forma seleccionada: ",forma)

                if int(forma) == 1:
                    AMPDU, AMPDUint = cifrarNORMAL(key)
                    packet = []
                    qoscontrol=b'\x00\x00'
                    packet.append(RadioTap() / Dot11(type=2, subtype=8, addr1=pkt.addr2, addr2=AP_MAC,
                                                     addr3=AP_MAC)/qoscontrol/AMPDU)
                    sendp(packet, iface=IFACE, verbose=False)
                if int(forma) == 2:
                    packet = []
                    qoscontrol = b'\x00\x00'
                    Hdr, mpduCi_Hex, mpduCi, ps, xs = cifrarCRT()
                    print(hexdump(mpduCi_Hex))
                    packet.append(RadioTap() / Dot11(type=2, subtype=8, addr1=pkt.addr2, addr2=AP_MAC,
                                                     addr3=AP_MAC) / qoscontrol / mpduCi_Hex)
                    sendp(packet, iface=IFACE, verbose=False)
                if int(forma) == 3:
                    calc_primos(3,128)

                #packet.append(RadioTap() / Dot11(type=2, subtype=8, FCfield="from-DS", addr1=pkt.addr3, addr2=AP_MAC,addr3=AP_MAC) / Dot11QoS(A_MSDU_Present=1))
                #sendp(packet, iface=IFACE, verbose=False)
                print("Enviado paquete AMPDU")
                #Paquete Block ACK request
                exit()
                packet = []
                data = "\x01\x00\x00\x00"
                packet.append(RadioTap(present='Rate',Rate=int(rates)) / Dot11(type=1, subtype=8, addr1=pkt.addr2, addr2=AP_MAC) / data)
                sendp(packet, iface=IFACE, verbose=False)
                #s.close()
                print("Enviado correctamente Block ACK request")

    #Capturamos el Probe Request enviado por STA
    if pkt.haslayer(scapy.Dot11Elt) and pkt.type==0 and pkt.subtype == 4:
        infoProbRequest=pkt.getlayer(Dot11Elt)
        if pkt.subtype not in ap_list:
            if infoProbRequest.info.decode() == "ap0":
                ap_list.append(pkt.subtype)
                #Paquete Probe Response
                radio=pkt.getlayer(RadioTap)
                packet = []
                packet.append(
                    RadioTap(present='Rate+A_MPDU',Rate=18,A_MPDU_flags='KnownEOF',A_MPDU_ref=1298623) / Dot11(subtype=5, addr1=AP_MAC_2, addr2=AP_MAC,addr3=AP_MAC) / Dot11ProbeResp(cap="ESS+CFP") / Dot11Elt(ID='SSID',
                                                                                          info=infoProbRequest.info.decode()) /
                    Dot11Elt(ID='Supported Rates', info="\x82\x84\x8b\x0c\x12\x96\x18\x24") / Dot11Elt(ID='DSSS Set',info=chr(56)) /
                    Dot11EltHTCapabilities(SM_Power_Save=3, Short_GI_20Mhz=1, Tx_STBC=1, Rx_STBC=1, Max_A_MSDU=1,
                                           DSSS_CCK=1) /
                    Dot11Elt(ID='Extended Supported Rates', info="\xb0\x48\x60\x6c"))

                sendp(packet, iface=IFACE, verbose=False)
                print("Enviado correctamente Probe response..")


#SINCRONIZACION:
#Paquete BEACON :periódicamente desde un punto de acceso a anunciar su presencia y proporcionar el SSID, y otros parámetros para WNIC dentro del rango
#SSID = Service Set ID (AP’s nickname)
#Supported Rates (MegaBits/S)=  Velocidad de datos compatibles
#DSSS Set informacion del canalr sobre el cual se esta transmitiendo

packet = []
packet.append(RadioTap() / Dot11(subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=AP_MAC, addr3=AP_MAC)
              / Dot11Beacon(cap="ESS+CFP") / Dot11Elt(ID='SSID', info="apjulian") / Dot11Elt(ID='Supported Rates',
                                                                                        info="\x0c\x12\x18\x24\x30\x48\x60\x6c") /
              Dot11Elt(ID='DSSS Set', info=chr(56)))

#Enviamos el Beacon
sendp(packet, iface=IFACE, verbose=False)

#Almacenamos el valor de la velocidad de transmision que se ha elegido
rates=sys.argv[1]
forma=sys.argv[2]
print("Beacon enviado")
scapy.sniff(iface=IFACE, prn=PacketHandler, timeout=30000)
