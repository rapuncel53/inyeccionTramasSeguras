import matplotlib.pyplot as plt
import re

def leer_datos(archivo):
    tiempos = []
    airtimes_separados = []
    tiempos_totales_separados = []
    airtime_agrupacion = []
    tiempos_agrupaciones = []
    tiempo1=0
    with open(archivo, 'r') as file:
        
        for linea in file:
            if 'paquete numero' in linea:
                tiempo = float(re.search(r'Tiempo (\d+\.\d+)', linea).group(1))
                airtime = float(re.search(r'Taire (\d+\.\d+)', linea).group(1))
                if tiempo1==0:
                    tiempo1=tiempo
                tiempos.append(tiempo-tiempo1)
                airtimes_separados.append(airtime)
            elif 'Tiempo total en el aire de los paquetes por separado =' in linea:
                tiempo_total_separado = float(re.search(r'(\d+\.\d+)', linea).group(1))
                tiempos_totales_separados.append(tiempo_total_separado)
                tiempos_agrupaciones.append(tiempos[-1])
            elif 'Tiempo en el aire de la' in linea:
                tiempo_agrupado = float(re.search(r'(\d+\.\d+)', linea).group(1))
                airtime_agrupacion.append(tiempo_agrupado)
    
    print("tiempos", tiempos[0], " airtimes_separados", airtimes_separados[0], 
          " tiempos_totales_separados", tiempos_totales_separados[0], 
          " airtime_agrupacion", airtime_agrupacion[0])
    
    return tiempos, airtimes_separados, tiempos_totales_separados, airtime_agrupacion, tiempos_agrupaciones

def graficar(tiempos, airtimes_separados, tiempos_totales_separados, airtime_agrupacion, tiempos_agrupaciones):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    tiempos_envio_reales=[0]
    for i in range(len(tiempos)-1):
        Tenvio_anterior=tiempos[i]+airtimes_separados[0]
        tiempos_envio_reales.append(max(Tenvio_anterior,tiempos[i+1]))


    # Graficar Airtime de cada paquete como barras
    ax.bar(tiempos_envio_reales, [1] * len(tiempos), width=airtimes_separados, label='Airtime de cada paquete', alpha=0.6, align='edge')
    print("tiempos ",len(tiempos))
    # Graficar Tiempo total separado como barras
    ax.bar(tiempos_agrupaciones, [0.2] * len(tiempos_agrupaciones), width=tiempos_totales_separados, label='Airtimes individuales sumados ', alpha=0.6, align='edge')
    print("tiempos agrupaciones ",len(tiempos_agrupaciones))
    # Graficar Airtime con agrupación como barras
    ax.bar(tiempos_agrupaciones, [0.6] * len(tiempos_agrupaciones), width=airtime_agrupacion, label='Airtime con agrupación', alpha=0.6, align='edge')
    
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('la altura no indica nada')
    ax.set_title('Airtime y Tiempo total en función del tiempo')
    ax.legend()
    ax.set_xlim([0, 0.04])

    plt.tight_layout()
    plt.show()

archivo = 'airtime9RayM0.0006.txt'  # Cambia esto por el nombre de tu archivo
tiempos, airtimes_separados, tiempos_totales_separados, airtime_agrupacion, tiempos_agrupaciones = leer_datos(archivo)

# Comprobar si se han leído correctamente los datos
if tiempos and airtimes_separados and tiempos_totales_separados and airtime_agrupacion:
    graficar(tiempos, airtimes_separados, tiempos_totales_separados, airtime_agrupacion, tiempos_agrupaciones)
else:
    print("Error al leer los datos del archivo.")
