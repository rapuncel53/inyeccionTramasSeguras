import struct
from a_generarFicheroPaquetes import leer_datos_paquetes
from b_ordenarpaquetes import ordenarpaquetes

t1 = 125  
t2 = 141
t3 = 157
t4 = 173
t5 = 189
t6 = 205
t7 = 221
t8 = 237
t9 = 253
t10 = 269
t11 = 285
t12 = 301
t13 = 317
t14 = 333
t15 = 349
t16 = 365
t17 = 381
t18 = 397
t19 = 413
t20 = 429
t21 = 445
t22 = 461
t23 = 477
t24 = 493
t25 = 509
def colocarcabeceras(paquetes_ordenados):  #COLOCA LOS PAQUETES CON SUS CABECERAS 
    paquetes_cabeceras = {}
    
    for mac,paquete in paquetes_ordenados.items():
        
        paquetes_cabeceras[mac] = []
         
        if (len(paquete)-t1) <= 0:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', 0)+ paquetes_ordenados[mac])
        elif (len(paquete)-t1) < t1:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t1)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t2:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t2)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80')+ paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t3:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t3)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t4:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t4)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t5:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t5)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t6:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t6)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t7:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t7)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t8:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t8)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t9:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t9)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t10:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t10)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t11:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t11)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t12:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t12)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t13:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t13)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t14:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t14)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t15:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t15)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t16:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t16)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t17:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t17)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t18:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t18)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t19:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t19)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t20:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t20)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t21:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t21)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t22:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t22)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t23:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t23)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        elif (len(paquete)-t1) < t24:
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t24)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])
        else: # Para t25 y más allá
            paquetes_cabeceras[mac].append((b'\x80')+struct.pack('!H', t25)+ paquetes_ordenados[mac][:t1])
            paquetes_cabeceras[mac].append((b'\x80') + paquetes_ordenados[mac][t1:])

    return paquetes_cabeceras

# eth_paquetes = leer_datos_paquetes("datosPaquetes.txt")
# for paquetes in eth_paquetes:
#     ord_paquetes = ordenarpaquetes(paquetes)
#     cab_paquetes = colocarcabeceras(ord_paquetes)
#     print (cab_paquetes)