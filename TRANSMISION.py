import sys
from scapy.layers.dot11 import *
#from scapy.layers.dot11 import Dot11, LLC, RadioTap, Dot11Beacon, Dot11Elt, Dot11ProbeResp
from scapy.utils import hexdump
from LECTURADEPAQUETES import *
from funcionesbasica import *



IFACE = 'wlx00c0caa81a35'                   #Interfaz de la targeta de red del transmisor
AP_MAC = '00:c0:ca:a8:1a:35'               #Direccion mac del transmisor
AP_MAC_2 = '00:c0:ca:a4:73:7b'               #Direccion mac del receptor

with open("/home/proyecto/prueba_simple_inyeccion/prueb git/ProyectoTFG/claves128.txt", "r") as archivo:
    contenido = archivo.read()
ps, xs, Hdr = eval(contenido)

def PacketHandler(paquetes_cifrar):
	packet = []
	qoscontrol = b'\x00\x00'
	for mac, paquete in paquetes_cifrar:
		print("mac = " + mac)
		if (mac =="11:11:11:11:11:11") :
			print("hola1")
			mpduCi_Hex = cifrarCRTbasica(paquete, Hdr, ps[1], xs[1])
		if (mac =="22:22:22:22:22:22") :
			print("hola2")
			mpduCi_Hex = cifrarCRTbasica(paquete, Hdr, ps[2], xs[2])
		if (mac =="33:33:33:33:33:33") :
			print("hola3")
			mpduCi_Hex = cifrarCRTbasica(paquete, Hdr, ps[3], xs[3])
		
		
	print(hexdump(mpduCi_Hex))
	packet.append(RadioTap(present='Rate',Rate=int(rates)) / Dot11(type=2, subtype=8, addr1=AP_MAC_2, addr2=AP_MAC,
	addr3=AP_MAC) / qoscontrol / mpduCi_Hex)
	sendp(packet, iface=IFACE, verbose=False)
	



#Almacenamos el valor de la velocidad de transmision que se ha elegido
rates=sys.argv[1]
# forma=sys.argv[2]


archivo_pcap = "captura.pcap"  # Cambiar por la ruta correcta de tu archivo

# Llamar a la función para leer el archivo .pcap y obtener los paquetes
paquetes, ampdu = leer_paquetes_pcap(archivo_pcap)

paquetes_cifrar=montar_paquetes(ampdu)

PacketHandler(paquetes_cifrar)
