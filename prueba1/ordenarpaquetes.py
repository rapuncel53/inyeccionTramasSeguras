import struct
import sys


def ordenarpaquetes(paquetes):
    #ordenamos por macs destino
    macs = set() #coleccion de elementos unicos
    paquetes_ordenados = {}#diccionario
    for paquete in paquetes:
        if paquete.dst not in macs:                                     #para cada mac mira si es nueva
            macs.add(paquete.dst)                                       # Añadir la MAC a la lista de MACs conocidas
            paquetes_ordenados[paquete.dst] = []
        tamano = len(paquete.payload) 
        print(tamano)
        longitud_empaquetada = struct.pack('!H', tamano) 
        print("longitud")
        print(longitud_empaquetada)
        print("payload")
        print(type(paquete.payload))
        yepa = longitud_empaquetada+bytes(paquete.payload)
        paquetes_ordenados[paquete.dst].append(yepa)     #apila en un array el tamaño y el payload
    for mac, paquetes in paquetes_ordenados.items():
        paquetes_ordenados[mac] = b''.join(paquetes)
    return paquetes_ordenados                                                                             #HAY QUE PONERLO EN UN FORMATO BUENO
        
    #para unirlos todos 
    #'11:11:11:11:11:11': ["0078b'E\\x00\0078b'E\\x01\0078b'E\\x02"]
                           #hdr + paquete + hdr + paquete + ...
    # for mac, datos in paquetes_ordenados.items():
    #     paquetes_ordenados[mac] = [b''.join(datos)]
    # return paquetes_ordenados   

t1 = 125  
t2 = 141
t3 = 157

def colocarcabeceras(paquetes_ordenados):
    paquetes_cabeceras = {}
    #mac = list(paquetes_ordenados.keys())
    for mac,paquete in paquetes_ordenados.items():
        #print((b'\x80').type)
        #print((struct.pack('!H', t1)).type)
        #print((paquetes_ordenados[mac][:t1]).type)
        paquetes_cabeceras[mac] = []
        #print (paquete)
        # print (len(paquete))
        # print(struct.pack('!H', t1+3))
        # print("ola")
        # print(paquetes_ordenados[mac][:3])
        
        if (len(paquete)-t1)<=0:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t1)+ paquetes_ordenados[mac])
        elif (len(paquete)-t1)<t1:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t1)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H',0) + paquetes_ordenados[mac][t1:])
        elif t2>(len(paquete)-t1)>t1:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t2)  + paquetes_ordenados[mac][:t2])
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', 0)+paquetes_ordenados[mac][t2:])
        elif t3>(len(paquete)-t1)>t2:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t3) + paquetes_ordenados[mac][:t3])
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', 0)+paquetes_ordenados[mac][t3:])
        else:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', 0) + paquetes_ordenados[mac])
            
    return paquetes_cabeceras


def paquetesacifrar(paquetes_con_cabeceras):
    paquetes_a_cifrar = []
    xs = []
    ps = []
    Hdr = 2843796326746969865517775137331587486046904811886503323102856146256129856445998934622446266251760018784185737111736108364839797946641759100223128000616308091539303132799727619266259596828149083874517781740179944644935556803289876169647362898861310839047877703563616025850495911850867054594022211735083536843875628987627216327719706741910036986827677832845686557780528840150455730953809234694322995111692138428714417268185133762942049850455209445920069601946607745983683598930918306972219800721120122707225650964714727753960963676306745813930269021935324632162446815277154321124916795985950915416767654347652388677539 #


    # print("paquetes_con_cabeceras")
    # print(paquetes_con_cabeceras)
    for mac in paquetes_con_cabeceras:
        # print("mac")
        # print(mac)

        for paquete in paquetes_con_cabeceras[mac]:
            
            # print("paquete")
            # print(paquete)
            
            paquetes_a_cifrar.append(paquete)
            ps.append(claves(mac,len(paquete))[0])
            xs.append(claves(mac,len(paquete))[1])
             #crea un array con todo lo necesario para enviarlo a cifrar
    # print("paquetes_a_cifrar")
    # print(paquetes_a_cifrar)                                                                  #paquete y claves
    return paquetes_a_cifrar,ps,xs,Hdr

def claves(mac,tamaño):  
#leer las claves de un fichero y asignarlas aqui
    claveps = None
    clavexs = None
    # print(mac,tamaño)
    if mac == "11:11:11:11:11:11": 
        if tamaño <= 128:
            clavexs = 162641696091516711354211556504313789492276539894903560654850061102352680046571975856144080089858580805216451486339949465354338498662444902521605940296925017366972748949239254160056230494954551972497384533461272115799756192481663124800659661665930415258830734874188575675086797142924094886867789649568570784113
            #claveps = 179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137859                            
        if tamaño == 144:
            clave = 234
        if tamaño == 160:
            clave = 342
    if mac == "22:22:22:22:22:22": 
        if tamaño <= 128:
            claveps = 179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224138297
            clavexs = 61399178074524773430565901241694559220711007274323284472607589163181201571585007181498944759868586204994613337417720619026027371373947886777075291899664104753215745394775641079762048281259968303144162452093550720003208351240576429867347039637020447193776507077786691499993711232519678742967060919857299599755
        if tamaño == 144:
            clave = 34567
        if tamaño == 160:
            clave = 359657
    return claveps,clavexs

