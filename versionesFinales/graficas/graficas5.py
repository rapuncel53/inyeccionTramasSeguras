import matplotlib.pyplot as plt
import re

def leer_datos(archivo):
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

def graficar(tiempos_lectura_paquetes,retardos_paquetes,tiempos_lectura_paquetes_grandes,retardos_paquetes_grandes):
    fig, ax = plt.subplots(figsize=(12, 6))
    
   

    # Graficar Airtime de cada paquete como barras
    ax.plot(tiempos_lectura_paquetes, retardos_paquetes, label='retardo de envio paquetes sin agrupar', color='red', marker ="o")
    ax.plot(tiempos_lectura_paquetes_grandes, retardos_paquetes_grandes, label='retardo de envio paquetes grandes sin agrupar', color='blue', marker ="x")
   
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
tiempos_lectura_paquetes, tiempos_recepcion_paquetes, tiempos_lectura_paquetes_grandes, retardos_paquetes_grandes = leer_datos(archivo)

# Comprobar si se han leído correctamente los datos
if tiempos_lectura_paquetes and tiempos_recepcion_paquetes and tiempos_lectura_paquetes_grandes and retardos_paquetes_grandes:
    graficar(tiempos_lectura_paquetes, tiempos_recepcion_paquetes,tiempos_lectura_paquetes_grandes,retardos_paquetes_grandes)
else:
    print("Error al leer los datos del archivo.")
