#!/usr/bin/env python
# import scapy module
import sys
import scapy.all as scapy
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Elt, Dot11EltHTCapabilities, Dot11AssoReq
from scapy.sendrecv import sendp
from Generatramas import *
from Criptotramas import *
from datos import *

ap_list = []
IFACE2 = 'wlx00c0caa4737b'
AP_MAC_2 = '00:c0:ca:a4:73:7b'
AP_MAC= '00:c0:ca:a8:1a:35'
rate=0
key = b'\x01\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a\x03\x0a'
#ps = [1100645304239144332874899719259313845702512851699, 1100645304239144332874899719259330726252929972829,
#      18465764008605840127818093568353291822549225699331595729]  # Claves p
#xs = [469185440907188674086266365887713402920751416175, 469185440907188674086266365887713402920751416175,
#      7016009363412435780763082007262025939147461935248010908]  # Claves x
#Hdr = 15954397600484676080445144553223529992678013943537230069224121000855699303061777531981089406222510881421088752704688036147253082732657897862191895053631674856772128322391273493214154863018969779796561231280601263793302777253129776032382760813815413222441888256216530367314241202928278526289479100743111536202
#ps = [179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137859, 179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224138297, 179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224139329]  # Claves p
#xs = [61532612183151989766205930813815390561113443681681995968199490173335911003999835523462532284700903164815026579044079760856420774246591642260901445439556024314129223936683100465128572657093503929612010803385711998703274746779669296639247107519144430016244277254712761539919575437442485825044104359387159626929, 120781863151076811603081594916227825651416067084458792888542504637690763567576631037593224201000755476707793103068861009762577113930453708881018257354997989329587724231518046518710393730889967935611457708286584393144022526743144545050205260685693388951693551689347099298998954185105522421238538460149080238638, 161702939626961102214505275865271225206715896353268350766272671718496391264978431038625871186631352027387835432150896808568601625068134836123499346488984068808037198213510796804394267107018198782462497610069064651555240867118401607677903262347922945067400695320147133370330389756550130427661712676155559611346]  # Claves x
ps = [179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137859, 179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224139329]  # Claves p
xs = [61532612183151989766205930813815390561113443681681995968199490173335911003999835523462532284700903164815026579044079760856420774246591642260901445439556024314129223936683100465128572657093503929612010803385711998703274746779669296639247107519144430016244277254712761539919575437442485825044104359387159626929, 161702939626961102214505275865271225206715896353268350766272671718496391264978431038625871186631352027387835432150896808568601625068134836123499346488984068808037198213510796804394267107018198782462497610069064651555240867118401607677903262347922945067400695320147133370330389756550130427661712676155559611346]  # Claves x
Hdr=12314424523399710210377055948372200154747154392094740560503724206906022954002244618803685360758315659701276735008769000695511885412906532531089465728788755777024080035650333674571007093841665832408801892543453072679102516126499144572080316015256649831656764126714033757046360935953611148682454945422624310449049280714032644653811283481540567971641506162904269545062901200424985226375639476019497242470140928784573424919287449248685759321678318303711811796790211017166833329145702520802392138903041560116976916715063653113568534758725811860479016444823763434590746562056902647016766036466919171940638281511890168065335
def PacketHandler(pkt):
    # Capturamos el AMPDU
    #print("tipo",pkt.subtype)
    if pkt.type == 2 and pkt.subtype == 8 and pkt.addr1==AP_MAC_2:
        if pkt.subtype not in ap_list:
            ap_list.append(pkt.subtype)
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

            if int(forma) == 1 :
            #print("Longitud AMPDU_FINAL",len(AMPDU_FINAL))
                print("AMSDU CIFRADO", AMPDU_FINAL)
                MSDU, lapso = AMPDU_dec(intAMPDUfinal, key)
                descifrado = MSDU[0].to_bytes((MSDU[0].bit_length() + 7) // 8, byteorder='big')
                print("AMSDU DESCIFRADO", descifrado)
            if int(forma) == 2:
                MSDUs = AMSDU_dec(Hdr, intAMPDUfinal, ps, xs)
                print (MSDUs)
                #nuevo=MSDUs.to_bytes((MSDUs.bit_length() + 7) // 8, byteorder='big')
                for i in MSDUs:
                    print(hexdump(i.to_bytes((i.bit_length() + 7) // 8, byteorder='big')))
            exit()
            #MSDU, lapso = AMPDU_dec(int.from_bytes(ver, byteorder='big'), key)


    #Capturamos el ADDBA Request
    if pkt.type == 0 and pkt.subtype == 13:
        if pkt.subtype not in ap_list:
            print("recibo ADDBA: ",pkt.addr2, "  ", AP_MAC)
            if pkt.addr2 == AP_MAC:
                print("recibo ADDBA con la mac correcta")
                ap_list.append(pkt.subtype)
                # Paquete ADDBA Response
                packet = []
                data = "\x03\x01\x01\x00\x00\x00\x00\x00\x00"
                packet.append(RadioTap(present='Rate',Rate=int(rate)) / Dot11(subtype=13, addr1=pkt.addr2, addr2=AP_MAC_2, addr3=AP_MAC_2) / data)
                sendp(packet, iface=IFACE2, verbose=False)
                print("Envio correcto ADDBA Response")

    #Capturamos el Block ACK request enviado por el AP
    if pkt.type == 1 and pkt.subtype == 8:
        if pkt.subtype not in ap_list:
            if pkt.addr2== AP_MAC:
                ap_list.append(18)
                #Paquete Block ACK
                packet = []
                data = "\x05\x00\xb0\x03\x00\x00\x00\x00\x00\x00\x00\x00"
                packet.append(
                    RadioTap(present='Rate',Rate=int(rate)) / Dot11(type=1, subtype=9, addr1=pkt.addr2, addr2=AP_MAC_2, addr3=AP_MAC_2) / data)
                sendp(packet, iface=IFACE2, verbose=False)
                print("Envio correcto Block ACK")

    #Capturamos el Probe response enviado por el AP
    if pkt.haslayer(scapy.Dot11Elt) and pkt.type == 0 and pkt.subtype == 5:
        if pkt.subtype not in ap_list:
            infoPacket=pkt.getlayer(Dot11Elt)
            if infoPacket.info.decode() =="ap0":
                ap_list.append(pkt.subtype)
                packet = []

                packet.append(RadioTap(present='Rate',Rate=int(rate)) / Dot11(subtype=0, addr1=pkt.addr3, addr2=AP_MAC_2, addr3=AP_MAC_2)/Dot11AssoReq(cap="ESS+CFP+res14")/ Dot11Elt(ID='SSID', info=infoPacket.info.decode()) / Dot11Elt(ID='Supported Rates', info="\x82\x84\x8b\x0c\x12\x96\x18\x24") /
        Dot11Elt(ID='DSSS Set', info=chr(56)) / Dot11EltHTCapabilities(SM_Power_Save=3,
                                                                       Short_GI_20Mhz=1, Tx_STBC=1,
                                                                       Rx_STBC=1, Max_A_MSDU=1,
                                                                       DSSS_CCK=1))

                sendp(packet, iface=IFACE2, verbose=False)
                print("Envio correcto Association request")


    #Capturamos el BEACON enviado por el AP
    if pkt.haslayer(scapy.Dot11Elt) and pkt.type == 0 and pkt.subtype == 8:
        if pkt.subtype not in ap_list:
            infoBeacon = pkt.getlayer(Dot11Elt)
            # Paquete Probe Request
            if infoBeacon.info.decode() == "ap0":
                ap_list.append(0)
                packet = []
                packet.append(
                    RadioTap(present='Rate', Rate=18) / Dot11(subtype=4, addr1='ff:ff:ff:ff:ff:ff', addr2=AP_MAC_2,
                                                             addr3=AP_MAC_2) / Dot11Elt(
                        ID='SSID',
                        info=infoBeacon.info) /
                    Dot11Elt(ID='Supported Rates', info="\x82\x84\x8b\x0c\x12\x96\x18\x24") /
                    Dot11Elt(ID='Extended Supported Rates', info="\xb0\x48\x60\x6c"))
                # Enviamos el Probe request
                sendp(packet, iface=IFACE2, verbose=False)
                print("Envio correcto Probe request")

rate = sys.argv[1]
forma= sys.argv[2]

scapy.sniff(iface=IFACE2, prn=PacketHandler, timeout=30000)
