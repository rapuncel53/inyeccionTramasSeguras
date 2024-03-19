
#!/usr/bin/env python
# import scapy module
import sys
import scapy.all as scapy
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Elt, Dot11EltHTCapabilities, Dot11AssoReq
from scapy.sendrecv import sendp
#from Generatramas import *
#from Criptotramas import *
#from datos import *
from funcionesbasicaoriginal import *
 
ap_list = []
IFACE2 = 'wlx00c0caa4737b'
AP_MAC_2 = '00:c0:ca:a4:73:7b'#mac rx
AP_MAC= '00:c0:ca:a8:1a:35'#mac tx
rate=11
forma = 2
key = b'\x01\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a'

#CLAVES
ps = [179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137859, 
      179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224138297, 
      179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224139329]
xs = [118207959318671346915575425274520378714762884053238547522761731176486626739794131896819778042855412495877019689488412178440311294972372271961969527543008466264301553351498552942980514682127739145866641044872622863281377747534695434506927684935447472573792848072238191595699243973065161693017253476903750973522, 
      82014680142354232390469106986883432547476105845714451399841022619540067200183105478897296994717818236876535163411157472829935462273920328535502881676923001708232765494635183846834056955678518174642386344940685806925651949254129812554432923212731563591321933393331825512793363986030705611650509226521891389163, 
      63793671105087392486896550159419068572504904449463592968901569824850431353300631156368380484873272077134825112914369461175236406888596416867023277581681028893453398091110759652739255008879701340399135033726288404711187357567515833066880879988169829451380825685249150706447705888816904655306766688336062394701]
Hdr = 2843796326746969865517775137331587486046904811886503323102856146256129856445998934622446266251760018784185737111736108364839797946641759100223128000616308091539303132799727619266259596828149083874517781740179944644935556803289876169647362898861310839047877703563616025850495911850867054594022211735083536843875628987627216327719706741910036986827677832845686557780528840150455730953809234694322995111692138428714417268185133762942049850455209445920069601946607745983683598930918306972219800721120122707225650964714727753960963676306745813930269021935324632162446815277154321124916795985950915416767654347652388677539

def PacketHandler(pkt):     #RECEPCION DE SIEMPRE
    # Capturamos el AMPDU
    #print("tipo",pkt.subtype)
    if pkt.type == 2 and pkt.subtype == 8 and pkt.addr1==AP_MAC_2:
        if pkt.subtype not in ap_list:
            #ap_list.append(pkt.subtype)
            ver=pkt.getlayer(Dot11)
            print("LONGITUD ENTRADA RADIO",len(ver))
            print(hexdump(ver))
            n=0
            numero=int.from_bytes(ver, byteorder='big')
            hexa=numero.to_bytes((numero.bit_length() + 7) // 8, byteorder='big')
            print("LONGITUD conversion entrada", len(hexa))

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
            print(hexdump(AMPDU_FINAL))
            intAMPDUfinal=int.from_bytes(AMPDU_FINAL, byteorder='big')

            if int(forma) == 2:
                MSDUs = AMSDU_dec_limpia(Hdr, intAMPDUfinal, ps, xs)
                print (MSDUs)
                #nuevo=MSDUs.to_bytes((MSDUs.bit_length() + 7) // 8, byteorder='big')
                paquetes_recibidos = []
                for i in MSDUs:
                    x=i.to_bytes((i.bit_length() + 7) // 8, byteorder='big')
                    print(hexdump(x))
                    
                
            #exit()
            print("SALIMOS")
            
            #MSDU, lapso = AMPDU_dec(int.from_bytes(ver, byteorder='big'), key)

# rate = sys.argv[1]
# forma= sys.argv[2]

scapy.sniff(iface=IFACE2, prn=PacketHandler, timeout=30000)
 