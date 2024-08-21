import numpy as np
import random
from scapy.all import rdpcap
#quiero un import para leer pcaps
def generar_fichero(longitud_media, desviacion_maxima, tiempo, tasa, tipo_norma,proporcion_ocupacion):

    
    if tipo_norma == 'g':
        time_sif = 10
        if tasa == 6 or tasa == 9:
            time_slot = 20
            time_preamb_ack = 192
            time_preambulo = 192 
        elif tasa == 12 or tasa == 18:
            time_slot = 9
            time_preamb_ack = 96
            time_preambulo = 96
        else:
            time_slot = 9
            time_preamb_ack = 96
            time_preambulo = 96 
    
    if tipo_norma == 'b':
        time_sif = 10
        if tasa == 1 or tasa == 2:
            time_slot = 20
            time_preamb_ack = 192
            time_preambulo = 192
        elif tasa == 5.5 or tasa == 11:
            time_slot = 20
            time_preamb_ack = 96
            time_preambulo = 96
        else:
            time_slot = 20
            time_preamb_ack = 96
            time_preambulo = 96
    
    time_diff = time_slot * 2 + time_sif
    #time_backoff = random.randint(0, 31) * time_slot
    time_backoff = 15.5 * time_slot
    time_tx = (longitud_media+36) * 8 / tasa
    time_ack = 14 * 8 / tasa

    print("diff", time_diff,"sifs",time_sif, "backoff", time_backoff, "tx", time_tx, "ack", time_ack,"time preamb ack",time_preamb_ack)
    tiempo_entre_paquetes_medio = (time_diff + time_backoff + time_preambulo + time_tx + time_sif + time_preamb_ack + time_ack)/float(proporcion_ocupacion/100) #como es N hay que divir por 0.8
    num_paquetes=round(tiempo*10**6/tiempo_entre_paquetes_medio)
    print(tiempo_entre_paquetes_medio)
    
    
    
    ta=0
    xd = []
    output_file = open(f"/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba6/datosPaquetes/{longitud_media}_{desviacion_maxima}/datosPaquetes{longitud_media}_{desviacion_maxima}_{proporcion_ocupacion}.txt", "w")
    for paquete in range(num_paquetes):

        
        size = random.randint(longitud_media-desviacion_maxima, longitud_media+desviacion_maxima)
        #size = random.normalvariate(longitud_media, desviacion_tipica_media)
        # timestamp distribucion raileigh con media
        xd.append(np.random.rayleigh(tiempo_entre_paquetes_medio/10**6/np.sqrt(np.pi/2)))
        timestamp = ta + np.random.rayleigh(tiempo_entre_paquetes_medio/10**6/np.sqrt(np.pi/2))
        #print(np.random.rayleigh(tiempo_entre_paquetes_medio/10**6/np.sqrt(np.pi/2)))
        timestamp = round(timestamp, 6)
        #la destination  un numero aleatorio del 1 al 3
        destination = random.randint(1,3)
        output_file.write(f"{timestamp} {size} {destination}\n")
        ta = timestamp
        
    print("media",np.mean(xd))
    output_file.close()
    
        


    
    

generar_fichero(550, 200, 10, 11, 'b', 80)   
generar_fichero(550, 200, 10, 11, 'b', 90)
generar_fichero(550, 200, 10, 11, 'b', 100)
generar_fichero(550, 200, 10, 11, 'b', 110) 
    