import matplotlib.pyplot as plt
import re

import numpy as np

def leer_datos_agrupacion(archivo):
    tiempos_lectura_paquetes_agrupables = []
    npaquetes = 0
    tiempos_lectura_agrupacion_y_solitarios = []
    tiempos_lectura_paquetes_agrupables_y_solitarios = []
    retardos_agrupacion_y_solitarios = []
    tiempo_recepcion_anterior = 0
    tiempo1=None
    retardos_solitarios = []
    tiempos_lectura_solitarios = []

    valores_dobles = []
    
    npaquetes=0 
    with open(archivo, 'r') as file:
        
        for linea in file:
            if 'paquete numero' in linea:   
                tiempo = float(re.search(r'Tiempo (\d+\.\d+)', linea).group(1))#leo tiempo paquete
                airtime = float(re.search(r'Taire (\d+\.\d+)', linea).group(1))#leo airtime paquete
                if tiempo1==None:
                    tiempo1=tiempo
                tiempos_lectura_paquetes_agrupables.append(tiempo-tiempo1)#guardo los tiempos referenciados al primer paquete
                tiempos_lectura_paquetes_agrupables_y_solitarios.append(tiempo-tiempo1)#guardo los tiempos referenciados al primer paquete
                npaquetes+=1
            elif 'paquete individual' in linea:
                tiempo = float(re.search(r'Tiempo (\d+\.\d+)', linea).group(1))#leo tiempo paquete
                airtime = float(re.search(r'Taire (\d+\.\d+)', linea).group(1))#leo airtime paquete
                if tiempo1==None:
                    tiempo1=tiempo
                tiempos_lectura_agrupacion_y_solitarios.append(tiempo-tiempo1)#guardo los tiempos referenciados al primer paquete
                tiempos_lectura_solitarios.append(tiempo-tiempo1)
                
            
                tiempos_lectura_paquetes_agrupables_y_solitarios.append(tiempo-tiempo1)#guardo los tiempos referenciados al primer paquete
                tiempo_recepcion = max(tiempo_recepcion_anterior, tiempos_lectura_agrupacion_y_solitarios[-1]) + airtime
                
                retardos_agrupacion_y_solitarios.append(tiempo_recepcion - tiempos_lectura_agrupacion_y_solitarios[-1])
                retardos_solitarios.append(tiempo_recepcion - tiempos_lectura_agrupacion_y_solitarios[-1])

                valores_dobles.append([tiempos_lectura_solitarios[-1], retardos_solitarios[-1]])

                #print("comparamos", retardos_agrupacion_y_solitarios[-1],tiempos_lectura_agrupacion_y_solitarios[-1])
                #print("comparamos solitarios",retardos_solitarios[-1],tiempos_lectura_solitarios[-1])

                tiempo_recepcion_anterior = tiempo_recepcion
            elif 'Tiempo total en el aire de los paquetes por separado =' in linea:
                airtime_suma = float(re.search(r'= (\d+\.\d+)', linea).group(1))#leo airtime suma de todos los paquetes agrupables
                tiempo = float(re.search(r'agrupacion (\d+\.\d+)', linea).group(1))#leo tiempo agrupacion
                tiempos_lectura_agrupacion_y_solitarios.append(tiempo-tiempo1)

            elif 'Tiempo en el aire de la' in linea:
                airtime_agrupacion = float(re.search(r'(\d+\.\d+)', linea).group(1))
                tiempo_recepcion = max(tiempo_recepcion_anterior,tiempos_lectura_agrupacion_y_solitarios[-1])+airtime_agrupacion
                
                #print("tiempo recepcion",tiempo_recepcion)
                for i in range(npaquetes):
                    retardos_agrupacion_y_solitarios.append(tiempo_recepcion-tiempos_lectura_paquetes_agrupables[-npaquetes+i])
                    valores_dobles.append([tiempos_lectura_paquetes_agrupables[-npaquetes+i], retardos_agrupacion_y_solitarios[-1]])

                npaquetes = 0
                tiempo_recepcion_anterior = tiempo_recepcion


    # print("tiempos lectura paquetes agrupables y solitarios",tiempos_lectura_paquetes_agrupables_y_solitarios)
    # print("retardos agrupacion y solitarios",retardos_agrupacion_y_solitarios)
    # print("tiempos lectura solitarios",tiempos_lectura_solitarios)
    # print("retardos solitarios",retardos_solitarios)
    # print("valores dobles",valores_dobles)
    
    # Extraer los valores x e y
    tiempos_lectura_paquetes_agrupables_y_solitarios = [pair[0] for pair in valores_dobles]
    retardos_agrupacion_y_solitarios = [pair[1] for pair in valores_dobles]


    return tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios

def leer_datos_sin_agrupar(archivo):
    tiempos_lectura_paquetes = []
    tiempos_lectura_paquetes_grandes = []
    retardos_paquetes = []
    retardos_paquetes_grandes = []
    tiempo_recepcion_anterior = 0
    tiempo1=None

    
    
    npaquetes=0 
    with open(archivo, 'r') as file:
        
        for linea in file:
            if 'paquete numero' in linea:   
                tiempo = float(re.search(r'Tiempo (\d+\.\d+)', linea).group(1))#leo tiempo paquete
                airtime = float(re.search(r'Taire (\d+\.\d+)', linea).group(1))#leo airtime paquete
                if tiempo1==None:
                    tiempo1=tiempo
                tiempos_lectura_paquetes.append(tiempo-tiempo1)#guardo los tiempos referenciados al primer paquete
                tiempo_recepcion = max(tiempo_recepcion_anterior,tiempos_lectura_paquetes[-1])+airtime
                retardos_paquetes.append(tiempo_recepcion-tiempos_lectura_paquetes[-1])
                tiempo_recepcion_anterior = tiempo_recepcion
            elif 'paquete individual' in linea:
                tiempo = float(re.search(r'Tiempo (\d+\.\d+)', linea).group(1))#leo tiempo paquete
                airtime = float(re.search(r'Taire (\d+\.\d+)', linea).group(1))#leo airtime paquete
                if tiempo1==None:
                    tiempo1=tiempo
                tiempos_lectura_paquetes.append(tiempo-tiempo1)#guardo los tiempos referenciados al primer paquete
                tiempos_lectura_paquetes_grandes.append(tiempo-tiempo1)#guardo los tiempos referenciados al primer paquete
                tiempo_recepcion = max(tiempo_recepcion_anterior,tiempos_lectura_paquetes[-1])+airtime
                retardos_paquetes.append(tiempo_recepcion-tiempos_lectura_paquetes[-1])
                retardos_paquetes_grandes.append(tiempo_recepcion-tiempos_lectura_paquetes[-1])
                tiempo_recepcion_anterior = tiempo_recepcion


    
    
    return tiempos_lectura_paquetes,  retardos_paquetes, tiempos_lectura_paquetes_grandes,retardos_paquetes_grandes

def graficar(tiempos_lectura_paquetes,retardos_paquetes,tiempos_lectura_paquetes_grandes,retardos_paquetes_grandes,tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    #calcular  media y desviacion retardos paquetes sin agrupar
    media_retardos_sin_agrupar = []
    tiempos_media_retardos_sin_agrupar = []
    suma_retardos = 0
    x=0
    numero_ultimo_paquete=0
    desviacion_estandar_sin_agrupar=[]
    for i in range(len(retardos_paquetes)):
        
        if(tiempos_lectura_paquetes[i] < x+1):
            suma_retardos += retardos_paquetes[i]
        else:
            media_retardos_sin_agrupar.append(suma_retardos/len(retardos_paquetes[numero_ultimo_paquete:i]))
            desviacion_estandar_sin_agrupar.append(np.std(retardos_paquetes[numero_ultimo_paquete:i]))
            numero_ultimo_paquete=i
            tiempos_media_retardos_sin_agrupar.append(x+0.5)
            suma_retardos = retardos_paquetes[i]
            x += 1

    #ax.plot(tiempos_media_retardos, media_retardos, color='green', label='media retardos agrupables y solitarios (envio sin agrupar)', marker='o')
    

    #calcular  media y desviacion retardos paquetes agrupando
    media_retardos_agrupando = []
    tiempos_media_retardos_agrupando = []
    suma_retardos = 0
    x=0
    numero_ultimo_paquete=0
    desviacion_estandar_agrupando=[]
    for i in range(len(retardos_agrupacion_y_solitarios)):
        
        if(tiempos_lectura_paquetes_agrupables_y_solitarios[i] < x+1):
            suma_retardos += retardos_agrupacion_y_solitarios[i]
        else:
            media_retardos_agrupando.append(suma_retardos/len(retardos_agrupacion_y_solitarios[numero_ultimo_paquete:i]))
            desviacion_estandar_agrupando.append(np.std(retardos_agrupacion_y_solitarios[numero_ultimo_paquete:i]))
            numero_ultimo_paquete=i
            tiempos_media_retardos_agrupando.append(x+0.5)
            suma_retardos = retardos_agrupacion_y_solitarios[i]
            x += 1
    
    
    



    

    # Graficar Airtime de cada paquete como barras
    if retardos_paquetes:
        ax.plot(tiempos_lectura_paquetes, retardos_paquetes, label='retardo de envio paquetes (envio sin agrupar)', color='yellow', marker ="o")
    if retardos_paquetes_grandes:
        ax.plot(tiempos_lectura_paquetes_grandes, retardos_paquetes_grandes, label='retardo de envio paquetes grandes (envio sin agrupar)', color='blue', marker ="x")
    if retardos_agrupacion_y_solitarios:
        ax.plot(tiempos_lectura_paquetes_agrupables_y_solitarios, retardos_agrupacion_y_solitarios, label='retardo de envio paquetes (envio agrupando)', color='orange', marker ="o")
    if retardos_solitarios:
        ax.plot(tiempos_lectura_solitarios, retardos_solitarios, label='retardo de envio paquetes grandes (envio agrupando) ', color='green', marker ="x")
    

    #ax.errorbar(tiempos_media_retardos_sin_agrupar, media_retardos_sin_agrupar, yerr=desviacion_estandar_sin_agrupar, fmt='o', label='desviacion estandar retardos agrupables y solitarios (envio sin agrupar)', ecolor='r', capsize=5)
    #ax.errorbar(tiempos_media_retardos_agrupando, media_retardos_agrupando, yerr=desviacion_estandar_agrupando, fmt='o', label='desviacion estandar retardos agrupables y solitarios (envio agrupando)', ecolor='b', capsize=5)


    ax.set_xlabel('Tiempos de lectura (segundos)')
    ax.set_ylabel('retardos de envio (segundos)')
    ax.set_title('retardos de envio paquetes ')
    ax.legend()

    plt.tight_layout()
    plt.show()

    # Guardar la gráfica en un archivo
    #plt.savefig('rayleigh_distribution_mean_0.0005.png')  # Puedes cambiar la extensión y el nombre del archivo
    #plt.close()  # Cierra la figura
    
###################################################################################
archivo = 'airtime_Captura'  # Cambia esto por el nombre de tu archivo
###################################################################################
tiempos_lectura_paquetes,  retardos_paquetes, tiempos_lectura_paquetes_grandes,retardos_paquetes_grandes = leer_datos_sin_agrupar(archivo)
tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios = leer_datos_agrupacion(archivo)

# Comprobar si se han leído correctamente los datos
#if tiempos_lectura_paquetes and retardos_paquetes and tiempos_lectura_paquetes_grandes and retardos_paquetes_grandes and tiempos_lectura_paquetes_agrupables_y_solitarios and  retardos_agrupacion_y_solitarios and tiempos_lectura_solitarios and retardos_solitarios:
graficar(tiempos_lectura_paquetes,  retardos_paquetes, tiempos_lectura_paquetes_grandes,retardos_paquetes_grandes,tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios)
#else:
#    print("Error al leer los datos del archivo.")
