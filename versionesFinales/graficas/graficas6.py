import matplotlib.pyplot as plt
import re

def leer_datos(archivo):
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
                
                print("tiempo recepcion",tiempo_recepcion)
                for i in range(npaquetes):
                    retardos_agrupacion_y_solitarios.append(tiempo_recepcion-tiempos_lectura_paquetes_agrupables[-npaquetes+i])
                    valores_dobles.append([tiempos_lectura_paquetes_agrupables[-npaquetes+i], retardos_agrupacion_y_solitarios[-1]])

                npaquetes = 0
                tiempo_recepcion_anterior = tiempo_recepcion


    print("tiempos lectura paquetes agrupables y solitarios",tiempos_lectura_paquetes_agrupables_y_solitarios)
    print("retardos agrupacion y solitarios",retardos_agrupacion_y_solitarios)
    print("tiempos lectura solitarios",tiempos_lectura_solitarios)
    print("retardos solitarios",retardos_solitarios)
    print("valores dobles",valores_dobles)
    
    # Extraer los valores x e y
    tiempos_lectura_paquetes_agrupables_y_solitarios = [pair[0] for pair in valores_dobles]
    retardos_agrupacion_y_solitarios = [pair[1] for pair in valores_dobles]


    return tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios

def graficar(tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios):
    fig, ax = plt.subplots(figsize=(12, 6))
    
   

    # Graficar Airtime de cada paquete como barras
    ax.plot(tiempos_lectura_paquetes_agrupables_y_solitarios, retardos_agrupacion_y_solitarios, label='retardo de envio paquetes agrupando', color='red', marker ="o")
    ax.plot(tiempos_lectura_solitarios, retardos_solitarios, label='retardo de envio paquetes grandes ', color='blue', marker ="x")
   
    ax.set_xlabel('Tiempos de lectura')
    ax.set_ylabel('retardos de envio(tiempo de recepcion - tiempo de lectura)')
    ax.set_title('retardos de envio paquetes sin agrupar')
    ax.legend()

    plt.tight_layout()
    plt.show()

    # Guardar la gráfica en un archivo
    #plt.savefig('rayleigh_distribution_mean_0.0005.png')  # Puedes cambiar la extensión y el nombre del archivo
    #plt.close()  # Cierra la figura
    

archivo = 'airtimenuevo.txt'  # Cambia esto por el nombre de tu archivo
tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios = leer_datos(archivo)

# Comprobar si se han leído correctamente los datos
if tiempos_lectura_paquetes_agrupables_y_solitarios and retardos_agrupacion_y_solitarios and tiempos_lectura_solitarios and retardos_solitarios:
    graficar(tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios)
else:
    print("Error al leer los datos del archivo.")
