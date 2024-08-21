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
    fig, axs = plt.subplots(3, 1, figsize=(7, 10))
    porcentaje_ocupado_por_paquete=[]
    porcentaje_ocupado_por_agrupacion=[]
    porcentaje_ocupado_separado_sumado=[]
    for i in range(len(airtimes_separados)-1):
        print("tiempos[i+1]",tiempos[i+1],"tiempos[i]",tiempos[i],"i",i)
        if tiempos[i+1]<=tiempos[i]:
            tiempos[i]=tiempos[i]-0.000001
            print("entro",tiempos[i])
            
        print("tiempos[i+1]",tiempos[i+1],"tiempos[i]",tiempos[i],"i",i)
        porcentaje_ocupado_por_paquete.append(airtimes_separados[i]/(tiempos[i+1]-tiempos[i])*100)
    for i in range(len(airtime_agrupacion)-1):
        porcentaje_ocupado_por_agrupacion.append(airtime_agrupacion[i]/(tiempos_agrupaciones[i+1]-tiempos_agrupaciones[i])*100)
        porcentaje_ocupado_separado_sumado.append(tiempos_totales_separados[i]/(tiempos_agrupaciones[i+1]-tiempos_agrupaciones[i])*100)
        
    # Graficar Airtime de cada paquete
    axs[0].plot(tiempos[:-1], porcentaje_ocupado_por_paquete, color='red', label='Airtime de cada paquete', marker='o')
    #axs[0].set_xlabel('Tiempo')
    axs[0].set_title('porcentaje de ocupación de airtime por paquete')
    axs[0].set_ylabel('paquetes por separado')
    axs[0].legend()

    # Graficar Tiempo total separado
    axs[1].plot(tiempos_agrupaciones[:-1], porcentaje_ocupado_separado_sumado, color='green', label='Tiempo total separado', marker='x')
    #axs[1].set_xlabel('Tiempo')
    axs[1].set_title('porcentaje de ocupación de airtime por paquete')
    axs[1].set_ylabel('suma de paquetes')
    axs[1].legend()

    # Graficar Airtime con agrupación
    axs[2].plot(tiempos_agrupaciones[:-1], porcentaje_ocupado_por_agrupacion, color='blue', label='Airtime con agrupación', marker='s')
    #axs[2].set_xlabel('Tiempo')
    axs[2].set_title('porcentaje de ocupación de airtime por paquete')
    axs[2].set_ylabel('paquetes agrupados')
    axs[2].legend()

    plt.tight_layout()
    plt.show()

archivo = 'airtime9RayM0.0006.txt'  # Cambia esto por el nombre de tu archivo
tiempos, airtimes_separados, tiempos_totales_separados, airtime_agrupacion, tiempos_agrupaciones = leer_datos(archivo)

# Comprobar si se han leído correctamente los datos
if tiempos and airtimes_separados and tiempos_totales_separados and airtime_agrupacion:
    graficar(tiempos, airtimes_separados, tiempos_totales_separados, airtime_agrupacion, tiempos_agrupaciones)
else:
    print("Error al leer los datos del archivo.")

