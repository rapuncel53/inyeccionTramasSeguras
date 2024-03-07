def ordenarpaquetes(paquetes):
    #ordenamos por macs destino
    macs = set() #coleccion de elementos unicos
    paquetes_ordenados = {}#diccionario
    for paquete in paquetes:
        if paquete.dst not in macs:                                     #para cada mac mira si es nueva
            macs.add(paquete.dst)                                       # Añadir la MAC a la lista de MACs conocidas
            paquetes_ordenados[paquete.dst] = []
        tamano = format(len(paquete.payload), '04X')    
        paquetes_ordenados[paquete.dst].append(str(tamano)+str(paquete.payload))     #apila en un array el tamaño y el payload
                                                                                     #HAY QUE PONERLO EN UN FORMATO BUENO
        
    #para unirlos todos 
    #'11:11:11:11:11:11': ["0078b'E\\x00\0078b'E\\x01\0078b'E\\x02"]
                           #hdr + paquete + hdr + paquete + ...
    for mac, datos in paquetes_ordenados.items():
        paquetes_ordenados[mac] = [''.join(datos)]
    return paquetes_ordenados   

t1 = 126
t2 = 142
t3 = 158

def colocarcabeceras(paquetes_ordenados):
    
    mac = list(paquetes_ordenados.keys())
    for mac,paquete in paquetes_ordenados.items():
        
        if (len(paquete)-t1)<t1:
            paquetes_ordenados[mac]= 1+t1 + paquetes_ordenados[mac][:t1]+1+0+paquetes_ordenados[mac][t1:]
        elif t2>(len(paquete)-t1)>t1:
            paquetes_ordenados[mac]= 1+t2 + paquetes_ordenados[mac][:t2]+1+0+paquetes_ordenados[mac][t2:]
        elif t3>(len(paquete)-t1)>t2:
            paquetes_ordenados[mac]= 1+t3 + paquetes_ordenados[mac][:t3]+1+0+paquetes_ordenados[mac][t3:]
        else:
            paquetes_ordenados[mac] =1+0+paquetes_ordenados[mac]
    return paquetes_ordenados

Hdr = 1231231 #

def paquetesacifrar(paquetes_con_cabeceras):
    paquetes_a_cifrar = []
    for mac, paquete in paquetes_con_cabeceras.items():
        paquetes_a_cifrar.append([paquete,claves(mac,len(paquete)),Hdr])  #crea un array con todo lo necesario para enviarlo a cifrar
                                                                          #paquete y claves
    return paquetes_a_cifrar

def claves(mac,tamaño):  

    if mac == "11:11:11:11:11:11": 
        if tamaño == 128:
            clave = 123                               #leer las claves de un fichero y asignarlas aqui
        if tamaño == 144:
            clave = 234
        if tamaño == 160:
            clave = 342
    if mac == "22:22:22:22:22:22": 
        if tamaño == 128:
            clave = 5678
        if tamaño == 144:
            clave = 34567
        if tamaño == 160:
            clave = 359657
    return clave

