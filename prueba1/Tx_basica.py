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
#from funcionesbasica import *
from ordenarpaquetes import ordenarpaquetes, colocarcabeceras, paquetesacifrar
from crearpaquetes import *
from funcionesbasicaoriginal import *


ap_list = []                                #Lista de indices para controlar que paquetes nos han llegado
IFACE = 'wlx00c0caa81a35'                   #Interfaz de la targeta de red del transmisor
AP_MAC = '00:c0:ca:a8:1a:35'               #Direccion mac del transmisor
AP_MAC_2= '00:c0:ca:a4:73:7b'               #Direccion mac del receptor()
rates=11                                     #Velocidad de transmision
forma=2
#key = secrets.token_bytes(16)  # Aquí debería coger una clave asociada al receptor
key = b'\x01\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a'

# ps = [179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137859,179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224138297]
# xs = [162641696091516711354211556504313789492276539894903560654850061102352680046571975856144080089858580805216451486339949465354338498662444902521605940296925017366972748949239254160056230494954551972497384533461272115799756192481663124800659661665930415258830734874188575675086797142924094886867789649568570784113,61399178074524773430565901241694559220711007274323284472607589163181201571585007181498944759868586204994613337417720619026027371373947886777075291899664104753215745394775641079762048281259968303144162452093550720003208351240576429867347039637020447193776507077786691499993711232519678742967060919857299599755]
# Hdr = 2843796326746969865517775137331587486046904811886503323102856146256129856445998934622446266251760018784185737111736108364839797946641759100223128000616308091539303132799727619266259596828149083874517781740179944644935556803289876169647362898861310839047877703563616025850495911850867054594022211735083536843875628987627216327719706741910036986827677832845686557780528840150455730953809234694322995111692138428714417268185133762942049850455209445920069601946607745983683598930918306972219800721120122707225650964714727753960963676306745813930269021935324632162446815277154321124916795985950915416767654347652388677539


#sendp(packet, iface=IFACE, verbose=False)

def PacketHandler(paquetes,ps,xs,Hdr):
	print("Forma seleccionada: ",forma)
	if int(forma) == 2:
		packet = []
		print ("holaforma2")
		qoscontrol = b'\x00\x00'
		#[int.from_bytes(paquete[0], byteorder='big')],paquete[1][0],paquete[1][1],paquete[2]
		
		Hdr1, mpduCi, ps1, xs1 = cifrarCRTbasica(paquetes,ps,xs,Hdr)#tiene que leer paquetes eth de un fichero e ir enviandolos
		print(hexdump(mpduCi))
		packet.append(RadioTap(present='Rate',Rate=int(rates)) / Dot11(type=2, subtype=8, addr1=AP_MAC_2, addr2=AP_MAC,
		addr3=AP_MAC) / qoscontrol / mpduCi)
		sendp(packet, iface=IFACE, verbose=False)
	if int(forma) == 3:
		calcPRIMOS(1,1)


#Almacenamos el valor de la velocidad de transmision que se ha elegido
# rates=sys.argv[1]
# forma=sys.argv[2]
		
paquetes = CrearPaquetes()

#for paquete in paquetes:
    #print(paquete.dst)
    #print(len(paquete.payload))
    #print(paquete.payload)

paquetes_ordenados = ordenarpaquetes(paquetes)

#print("Paquetes ordenados:")
#print(paquetes_ordenados)

#{'11:11:11:11:11:11': b'\x00\x14E\x00\x00\x14\x00\x01\x00\x00@\x001\x18\x9b\xd2\x9d\xef\x08\x08\x08\x08\x00\x1cE\x00\x00\x1c\x00\x01\x00\x00@\x013\x11\x9b\xd2\x9d\xef\x07\x07\x07\x07\x08\x00\xf7\xff\x00\x00\x00\x00\x00\x1cE\x00\x00\x1c\x00\x01\x00\x00@\x015\x13\x9b\xd2\x9d\xef\x06\x06\x06\x06\x08\x00\xf7\xff\x00\x00\x00\x00', '22:22:22:22:22:22': b'\x00\x1cE\x00\x00\x1c\x00\x01\x00\x00@\x017\x15\x9b\xd2\x9d\xef\x05\x05\x05\x05\x08\x00\xf7\xff\x00\x00\x00\x00\x00\x1cE\x00\x00\x1c\x00\x01\x00\x00@\x019\x17\x9b\xd2\x9d\xef\x04\x04\x04\x04\x08\x00\xf7\xff\x00\x00\x00\x00'}


# Obtener la primera dirección MAC de los paquetes ordenados
if paquetes_ordenados:
    mac = list(paquetes_ordenados.keys())[0]
    #print("MAC:", mac)

paquetes_con_cabeceras = colocarcabeceras(paquetes_ordenados)
print("Paquetes con cabeceras:")
print(paquetes_con_cabeceras)
paquetes_a_cifrar,ps0,xs0,Hdr = paquetesacifrar(paquetes_con_cabeceras)
print("Paquetes a cifrar:")
# pide (paquete, ps, xs, Hdr)(array con los paquetes en enteros)(array con las claves)(Hdr)
datos_array = list(paquetes_con_cabeceras.values())
print("Array de paquetes",datos_array)

for paquete in paquetes_a_cifrar:
	print("paquetes_a_cifrar ")
	print(hexdump(paquete))
	
print("paquetes",paquetes_a_cifrar)
print("ps0",ps0,"xs0",xs0)



PacketHandler(paquetes_a_cifrar,ps0,xs0,Hdr)
