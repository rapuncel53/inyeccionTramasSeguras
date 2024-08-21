import matplotlib.pyplot as plt
import re

import numpy as np

def leer_datos_agrupacion(archivo):

    airtimes_agrupaciones_y_solitarios, tiempos_envio_agrupaciones_y_solitarios = [], []
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



                
                airtimes_agrupaciones_y_solitarios.append(airtime)






                if tiempo1==None:
                    tiempo1=tiempo
                tiempos_lectura_agrupacion_y_solitarios.append(tiempo-tiempo1)#guardo los tiempos referenciados al primer paquete
                tiempos_lectura_solitarios.append(tiempo-tiempo1)
                
            
                tiempos_lectura_paquetes_agrupables_y_solitarios.append(tiempo-tiempo1)#guardo los tiempos referenciados al primer paquete
                tiempo_recepcion = max(tiempo_recepcion_anterior, tiempos_lectura_agrupacion_y_solitarios[-1]) + airtime

                tiempos_envio_agrupaciones_y_solitarios.append(max(tiempo_recepcion_anterior, tiempos_lectura_agrupacion_y_solitarios[-1]))
                
                retardos_agrupacion_y_solitarios.append(tiempo_recepcion - tiempos_lectura_agrupacion_y_solitarios[-1])
                retardos_solitarios.append(tiempo_recepcion - tiempos_lectura_agrupacion_y_solitarios[-1])

                valores_dobles.append([tiempos_lectura_solitarios[-1], retardos_solitarios[-1]])

                print("comparamos", retardos_agrupacion_y_solitarios[-1],tiempos_lectura_agrupacion_y_solitarios[-1])
                print("comparamos solitarios",retardos_solitarios[-1],tiempos_lectura_solitarios[-1])

                tiempo_recepcion_anterior = tiempo_recepcion
            elif 'Tiempo total en el aire de los paquetes por separado =' in linea:
                airtime_suma = float(re.search(r'= (\d+\.\d+)', linea).group(1))#leo airtime suma de todos los paquetes agrupables
                tiempo = float(re.search(r'agrupacion (\d+\.\d+)', linea).group(1))#leo tiempo agrupacion
                tiempos_lectura_agrupacion_y_solitarios.append(tiempo-tiempo1)

            elif 'Tiempo en el aire de la' in linea:
                airtime_agrupacion = float(re.search(r'(\d+\.\d+)', linea).group(1))
                tiempo_recepcion = max(tiempo_recepcion_anterior,tiempos_lectura_agrupacion_y_solitarios[-1])+airtime_agrupacion


                tiempos_envio_agrupaciones_y_solitarios.append(max(tiempo_recepcion_anterior,tiempos_lectura_agrupacion_y_solitarios[-1]))



                airtimes_agrupaciones_y_solitarios.append(airtime_agrupacion)





        
                
                print("tiempo recepcion",tiempo_recepcion)
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


    return tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios, airtimes_agrupaciones_y_solitarios, tiempos_envio_agrupaciones_y_solitarios
def leer_datos_sin_agrupar(archivo):
    tiempos_lectura_paquetes = []
    tiempos_lectura_paquetes_grandes = []
    retardos_paquetes = []
    retardos_paquetes_grandes = []
    tiempo_recepcion_anterior = 0
    tiempo1=None
    airtimes_individuales_y_solitarios = []
    tiempos_envio_individuales_y_solitarios =  []

    
    
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
                airtimes_individuales_y_solitarios.append(airtime)
                tiempos_envio_individuales_y_solitarios.append(max(tiempo_recepcion_anterior,tiempos_lectura_paquetes[-1]))
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
                airtimes_individuales_y_solitarios.append(airtime)
                tiempos_envio_individuales_y_solitarios.append(max(tiempo_recepcion_anterior,tiempos_lectura_paquetes[-1]))
                retardos_paquetes.append(tiempo_recepcion-tiempos_lectura_paquetes[-1])
                retardos_paquetes_grandes.append(tiempo_recepcion-tiempos_lectura_paquetes[-1])
                tiempo_recepcion_anterior = tiempo_recepcion


    
    
    return tiempos_lectura_paquetes,  retardos_paquetes, tiempos_lectura_paquetes_grandes,retardos_paquetes_grandes, airtimes_individuales_y_solitarios, tiempos_envio_individuales_y_solitarios


def graficar(airtimes_agrupaciones_y_solitarios, tiempos_envio_agrupaciones_y_solitarios, airtimes_individuales_y_solitarios, tiempos_envio_individuales_y_solitarios):
    fig, ax = plt.subplots( figsize=(12, 6))
    porcentaje_airtime_usado = []
    tiempos_porcentaje_airtime_usado = []
    suma_airtimes = 0
    x=0
    print(len(tiempos_envio_agrupaciones_y_solitarios))
    for i in range(len(tiempos_envio_agrupaciones_y_solitarios)):
        print(tiempos_envio_agrupaciones_y_solitarios[i])
        if(tiempos_envio_agrupaciones_y_solitarios[i] < x+0.01):
            suma_airtimes += airtimes_agrupaciones_y_solitarios[i]
        else:
            porcentaje_airtime_usado.append(suma_airtimes/0.01)
            tiempos_porcentaje_airtime_usado.append(x+0.005)
            suma_airtimes = airtimes_agrupaciones_y_solitarios[i]
            x += 0.01

    ax.plot(tiempos_porcentaje_airtime_usado, porcentaje_airtime_usado, color='green', label='porcentaje de airtime usado con agrupaciones', marker='o')

    #---------------------------------------------------------------------------------

    # Graficar Airtime de cada paquete
    #ax.plot(tiempos_envio_agrupaciones_y_solitarios,[1] * len(tiempos_envio_agrupaciones_y_solitarios), color='red', label='Airtime de cada paquete', marker='o')
    #ax.bar(tiempos_envio_agrupaciones_y_solitarios, [1] * len(tiempos_envio_agrupaciones_y_solitarios), width=airtimes_agrupaciones_y_solitarios,edgecolor='darkblue', label='Airtime de cada paquete', alpha=0.6, align='edge')
    #axs[0].set_xlabel('Tiempo')
    ax.set_title('porcentaje de ocupación de airtime por paquete')
    ax.set_ylabel('paquetes por separado')
    ax.legend()
    #ax.set_xlim([0, 0.6])
    

    
    nombre_archivo = 'grafica1_cambiar_nombre.svg'  # Puedes cambiar la extensión a .pdf, .svg, .jpg, etc.
    plt.savefig(nombre_archivo)
    plt.tight_layout()
    plt.show()

def graficar2( airtimes_individuales_y_solitarios, tiempos_envio_individuales_y_solitarios):
    fig, ax = plt.subplots( figsize=(12, 6))
   

    #---------------------------------------------------------------------------------

    porcentaje_airtime_usado = []
    tiempos_porcentaje_airtime_usado = []
    suma_airtimes = 0
    x=0
    
    for i in range(len(tiempos_envio_individuales_y_solitarios)):
        
        if(tiempos_envio_individuales_y_solitarios[i] < x+1):
            suma_airtimes += airtimes_individuales_y_solitarios[i]
        else:
            porcentaje_airtime_usado.append(suma_airtimes/1)
            tiempos_porcentaje_airtime_usado.append(x)
            suma_airtimes = airtimes_individuales_y_solitarios[i]
            x += 1

    ax.plot(tiempos_porcentaje_airtime_usado, porcentaje_airtime_usado, color='orange', label='porcentaje de airtime usado sin agrupaciones', marker='o')
    
    # media = np.mean(porcentaje_airtime_usado)
    # desviacion_estandar = np.std(porcentaje_airtime_usado)
    # print("media",media,"desviacion_estandar",desviacion_estandar)
    # ax.errorbar(range(len(porcentaje_airtime_usado)), porcentaje_airtime_usado, yerr=desviacion_estandar, fmt='o', label='Tamaño de Paquete', ecolor='r', capsize=5)


    # Graficar Airtime de cada paquete
    #ax.plot(tiempos_envio_individuales_y_solitarios,[1] * len(tiempos_envio_individuales_y_solitarios), color='red', label='Airtime de cada paquete', marker='o')
    #ax.bar(tiempos_envio_individuales_y_solitarios, [1] * len(tiempos_envio_individuales_y_solitarios), width=airtimes_individuales_y_solitarios,edgecolor='darkblue', label='Airtime de cada paquete', alpha=0.6, align='edge')
    #axs[0].set_xlabel('Tiempo')
    ax.set_title('porcentaje de ocupación de airtime por paquete')
    ax.set_ylabel('paquetes por separado')
    ax.legend()
    #ax.set_xlim([0, 0.6])
    

    
    nombre_archivo = 'grafica2_cambiar_nombre.pdf'  # Puedes cambiar la extensión a .pdf, .svg, .jpg, etc.
    plt.savefig(nombre_archivo)
    plt.tight_layout()
    plt.show()

##########################################################################
archivo = 'airtime350_200_90.txt'  # Cambia esto por el nombre de tu archivo
##########################################################################
tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios, airtimes_agrupaciones_y_solitarios, tiempos_envio_agrupaciones_y_solitarios = leer_datos_agrupacion(archivo)
tiempos_lectura_paquetes,  retardos_paquetes, tiempos_lectura_paquetes_grandes,retardos_paquetes_grandes, airtimes_individuales_y_solitarios, tiempos_envio_individuales_y_solitarios = leer_datos_sin_agrupar(archivo)

# Comprobar si se han leído correctamente los datos
if airtimes_individuales_y_solitarios and tiempos_envio_individuales_y_solitarios:
    
    graficar2(airtimes_individuales_y_solitarios, tiempos_envio_individuales_y_solitarios)
else:
    print("Error al leer los datos del archivo.1")

if airtimes_agrupaciones_y_solitarios and tiempos_envio_agrupaciones_y_solitarios and airtimes_individuales_y_solitarios and tiempos_envio_individuales_y_solitarios:
    
    graficar(airtimes_agrupaciones_y_solitarios, tiempos_envio_agrupaciones_y_solitarios, airtimes_individuales_y_solitarios, tiempos_envio_individuales_y_solitarios)
else:
    print("Error al leer los datos del archivo.2")

