# -*- coding: utf-8 -*-
import scapy.all as scapy
import sys
from scapy.layers.dot11 import *
from scapy.layers.dot11 import Dot11, LLC, RadioTap, Dot11Beacon, Dot11Elt, Dot11ProbeResp
from scapy.layers.inet import UDP
from scapy.packet import Raw
from scapy.utils import hexdump, checksum
#from datos import *
import pickle5 as pickle
from funcionesLimpias import *

ap_list = []                                #Lista de indices para controlar que paquetes nos han llegado
IFACE = 'wlx00c0caa81a35'                   #Interfaz de la targeta de red del transmisor
AP_MAC = '00:c0:ca:a8:1a:35'               #Direccion mac del transmisor
AP_MAC_2= '00:c0:ca:a4:73:7b'               #Direccion mac del receptor()
rates=0                                      #Velocidad de transmision
forma=0
#key = secrets.token_bytes(16)  # Aquí debería coger una clave asociada al receptor
key = b'\x01\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a'



#sendp(packet, iface=IFACE, verbose=False)

def PacketHandler():
	print("Forma seleccionada: ",forma)
	if int(forma) == 2:
		packet = []
		print ("holaforma2")
		qoscontrol = b'\x00\x00'
		Hdr, mpduCi_Hex, mpduCi, ps, xs = cifrarCRTlimpia()
		print(hexdump(mpduCi_Hex))
		packet.append(RadioTap(present='Rate',Rate=int(rates)) / Dot11(type=2, subtype=8, addr1=AP_MAC_2, addr2=AP_MAC,
		addr3=AP_MAC) / qoscontrol / mpduCi_Hex)
		sendp(packet, iface=IFACE, verbose=False)
	if int(forma) == 3:
		calcPRIMOS(3,128)


#Almacenamos el valor de la velocidad de transmision que se ha elegido
rates=sys.argv[1]
forma=sys.argv[2]
PacketHandler()
