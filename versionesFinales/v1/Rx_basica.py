
#!/usr/bin/env python
# import scapy module
import socket
import time
import sys
import scapy.all as scapy
from scapy.all import IP,Ether,Raw
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Elt, Dot11EltHTCapabilities, Dot11AssoReq
from scapy.sendrecv import sendp
#from Generatramas import *
#from Criptotramas import *
#from datos import *
from funcionesbasicaoriginal import *
from calcularclaves2 import claves
 
ap_list = []
IFACE2 = 'wlx00c0caa4737b'
AP_MAC_2 = '00:c0:ca:a4:73:7b'#mac rx
AP_MAC= '00:c0:ca:a8:1a:35'#mac tx
#rate=11
forma = 2

key = b'\x01\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a'


packet_count = 0

#CLAVES hay dos claves de 128 clave de 
# ps = [179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224138297, 
#       179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137859]
# xs = [177928423312439053995703481881258890244790761939370755203010759812980282998491239486966509494062109690571089389046420694154900059115354784359054738957907141672620485217115986879959012897361963934451628075681226606408014161864354889288929969841491808749976466620440871742831038132723566943966595056549102780803, 
#       44882287698419078613517452534315281755209171933070476169111588178949012668204816404603096993361801531676111354980161362890595093612479146301362593201332910192707815484885438192655268757816419516380481249246042531451631456537860592864336893480287500380140889826056423180273682193727278514502670858206046797524]
Hdr = 2843796326746969865517775137331587486046904811886503323102856146256129856445998934622446266251760018784185737111736108364839797946641759100223128000616308091539303132799727619266259596828149083874517781740179944644935556803289876169647362898861310839047877703563616025850495911850867054594022211735083536843875628987627216327719706741910036986827677832845686557780528840150455730953809234694322995111692138428714417268185133762942049850455209445920069601946607745983683598930918306972219800721120122707225650964714727753960963676306745813930269021935324632162446815277154321124916795985950915416767654347652388677539

def PacketHandler(pkt):     #RECEPCION DE SIEMPRE
    # Capturamos el AMPDU
    #print("tipo",pkt.subtype)

    paquetes_recuperados = []
    if pkt.haslayer(Dot11):
        dot11_layer = pkt.getlayer(Dot11)
        if pkt.type == 2 and pkt.subtype == 8 and pkt.addr1==AP_MAC_2:
            
            
            if pkt.subtype not in ap_list:
                #ap_list.append(pkt.subtype)
                ver=pkt.getlayer(Dot11)
                print("LONGITUD ENTRADA RADIO",len(ver))
                #print(hexdump(ver))
                n=0
                numero=int.from_bytes(ver, byteorder='big')
                hexa=numero.to_bytes((numero.bit_length() + 7) // 8, byteorder='big')
                print("LONGITUD conversion entrada", len(hexa))
                tiempo_actual = time.time()
                print("Paquete recibido en el tiempo:", tiempo_actual)

                AMPDU_FINAL = b''
                for i in hexa:
                    #print(hex(i))
                    if n<(len(hexa)-4) and n>=26:
                        if i != 0:
                            by = i.to_bytes((i.bit_length() + 7) // 8, byteorder='big')
                            AMPDU_FINAL = AMPDU_FINAL + by
                        else:
                            AMPDU_FINAL = AMPDU_FINAL + b'\x00'

                    n = n + 1
                #print(hexdump(AMPDU_FINAL))
                intAMPDUfinal=int.from_bytes(AMPDU_FINAL, byteorder='big')
                

                if int(forma) == 2:
                    global packet_count
                    packet_count += 1  # Increment the packet count
                    ps, xs = claves("22:22:22:22:22:22", -1)
                    MSDUs = AMSDU_dec_limpia(Hdr, intAMPDUfinal, [ps], [xs])
                    print (MSDUs)
                    paquetes_recibidos = None
                    x=MSDUs[0].to_bytes((MSDUs[0].bit_length() + 7) // 8, byteorder='big')
                    dst_ip_bytes = x[21:25]
                    dst_ip = socket.inet_ntoa(dst_ip_bytes)
                    print(f"Dirección IP de destino: {dst_ip}")
                        
                    if dst_ip == "2.2.2.2":
                        
                        paquetes_recibidos=x[3:]
                        print(hexdump(x))
                        clave_siguiente = int(x[1:3].hex(),16)
                        ps, xs = claves("22:22:22:22:22:22", clave_siguiente)
                        print("clave siguiente",clave_siguiente,"paquete numero ",packet_count)
                        if clave_siguiente != 0:
                            MSDUs = AMSDU_dec_limpia(Hdr, intAMPDUfinal, [ps], [xs])
                            x=MSDUs[0].to_bytes((MSDUs[0].bit_length() + 7) // 8, byteorder='big')
                            paquetes_recibidos+=x[1:]
                            print(hexdump(x))
                            print("paquetes_recibidos ",paquetes_recibidos)
                        
                    #nuevo=MSDUs.to_bytes((MSDUs.bit_length() + 7) // 8, byteorder='big')
                    
                    tam=0
                    tamaño_siguiente = 0
                    if paquetes_recibidos:
                        while len(paquetes_recibidos)>(tam):
                            tamaño_siguiente = int(paquetes_recibidos[tam:(tam+2)].hex(),16)
                            print(paquetes_recibidos[tam:(tam+2)])
                            print("Tamaño siguiente",tamaño_siguiente)
                            print("paquete recibido",paquetes_recibidos[(tam+2):(tam+2+tamaño_siguiente)])
                            paquetes_recuperados.append( b'\x00\x00\x00\x00\x00\x00\x16\x16\x16\x16\x16\x16\x9b\xd2'+paquetes_recibidos[(tam+2):(tam+2+tamaño_siguiente)])
                            #yield paquetes_recuperados
                            tam += tamaño_siguiente+2
                            
                        
                    
                #exit()
                if pkt.haslayer(Dot11):
                    radiotap = pkt.getlayer(RadioTap)
                    if radiotap and hasattr(radiotap, 'rate'):
                        rate = radiotap.rate / 2.0  # Scapy returns rate in 500 kbps units
                        print(f"Tasa de transmisión: {rate} Mbps")
                    else:
                        print("Paquete capturado sin tasa de transmisión")
                print("SALIMOS")
                # Save the packets to a pcap file
                packets = [Raw(load=byte_packet) for byte_packet in paquetes_recuperados]
                for packet in packets:
                    packet.time = tiempo_actual
                print("paquetes guardados con tiempo ",tiempo_actual)    
                scapy.wrpcap('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/versionesFinales/v1/paquetes_recuperados.pcap', packets, append=True)
                #MSDU, lapso = AMPDU_dec(int.from_bytes(ver, byteorder='big'), key)

# rate = sys.argv[1]
# forma= sys.argv[2]
scapy.wrpcap('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/versionesFinales/v1/paquetes_recuperados.pcap',[])
scapy.sniff(iface=IFACE2, prn=PacketHandler, timeout=30000)
 
