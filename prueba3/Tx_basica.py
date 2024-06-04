# -*- coding: utf-8 -*-
import scapy.all as scapy
import sys

sys.path.append('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba3/calcular eficiencia')
from scapy.layers.dot11 import *
from scapy.layers.dot11 import Dot11, LLC, RadioTap, Dot11Beacon, Dot11Elt, Dot11ProbeResp
from scapy.layers.inet import UDP
from scapy.packet import Raw
from scapy.utils import hexdump, checksum
#import pickle5 as pickle
from a_generarFicheroPaquetes import leer_datos_paquetes
from b_ordenarpaquetes import ordenarpaquetes
from c_colocarCabeceras import colocarcabeceras
from d_paquetesAcifrar import paquetesacifrar
from e_calcularClaves import *
from funcionesbasicaoriginal import *
from calculareficiencia2 import calculate_airtime

#from calcular eficiencia.calculareficiencia2 import calculate_airtime

ap_list = []                                #Lista de indices para controlar que paquetes nos han llegado
IFACE = 'wlx00c0caa81a35'                   #Interfaz de la targeta de red del transmisor
AP_MAC = '00:c0:ca:a8:1a:35'               #Direccion mac del transmisor
AP_MAC_2= '00:c0:ca:a4:73:7b'               #Direccion mac del receptor()
rates=600                                  #Velocidad de transmision por defecto
forma=11
ind = 0
#key = secrets.token_bytes(16)  # Aquí debería coger una clave asociada al receptor
key = b'\x01\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a'


def PacketHandler(paquetes,ps,xs,Hdr):
	#print("Forma seleccionada: ",forma)
	if int(forma) == 2:
		packet = []
		#print ("transmito en forma2")
		qoscontrol = b'\x00\x00'
		
		mpduCi = cifrarCRTbasica(paquetes,ps,xs,Hdr)#tiene que leer paquetes eth de un fichero e ir enviandolos
		#print(mpduCi)
		packet.append(RadioTap(present='Rate',Rate=int(rates)) / Dot11(type=2, subtype=8, addr1=AP_MAC_2, addr2=AP_MAC,
		addr3=AP_MAC) / qoscontrol / mpduCi)
		print("len mpduCi ",len(mpduCi))
		print("lenpaquete ",len(packet[0]))
		sendp(packet, iface=IFACE, verbose=False)
	if int(forma) == 3:
		calcPRIMOS(1,1)


#Almacenamos el valor de la velocidad de transmision que se ha elegido
# rates=sys.argv[1]
# forma=sys.argv[2]

eth_paquetes = leer_datos_paquetes("datosPaquetes2.txt")


#L=2
Rb = 11*10**6
DIFS = 50 * 10**(-6)
Backoff_medio = 310 * 10**(-6)
TDataPreambulo = TAckPreambulo = 96 * 10**(-6)
#TDataMac = (L+36)*8/Rb
SIFS = 10 * 10**(-6)
TAckMac = 14*8/Rb
for paquetes in eth_paquetes:
    ord_paquetes = ordenarpaquetes(paquetes)
    
    cab_paquetes = colocarcabeceras(ord_paquetes)
    
    cif_paquetes = paquetesacifrar(cab_paquetes)
    
    tamañocifrar = 0
    for paquete in cif_paquetes[0]:
        tamañocifrar += len(paquete)
        


    print ("tamaño total a cifrar",tamañocifrar)
    TDataMac = (tamañocifrar+36)*8/Rb
    Tpaquete = DIFS + Backoff_medio + TDataPreambulo +TDataMac + SIFS + TAckPreambulo + TAckMac
    #print("Valores : ",DIFS,Backoff_medio,TDataPreambulo,TDataMac,SIFS,TAckPreambulo,TAckMac)
    Tpaquete2 = calculate_airtime("802.11b", 11* 10**6, tamañocifrar)
    print("Tiempo en el aire de la agrupacion = ",Tpaquete)
    print("Tiempo en el aire de la agrupacionxd = ",Tpaquete2)
    #print("paquetesacifrar",cif_paquetes)
    Total = 0
    for paquete in cif_paquetes[0]:
        #print("tamaño ",len(paquete))
        Total += len(paquete)
    print("tamaño TOTAL ",Total)
    ind += 1
    print("paquete numero ",ind)
    PacketHandler(cif_paquetes[0],cif_paquetes[1],cif_paquetes[2],cif_paquetes[3])
	


