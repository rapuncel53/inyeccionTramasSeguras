import matplotlib.pyplot as plt
import re

def leer_datos(archivo):
    tiempos = []
    airtimes_separados = []
    airtime_agrupacion = []
    
    with open(archivo, 'r') as file:
        for linea in file:
            if 'paquete numero' in linea:
                tiempo = re.search(r'Tiempo (\d+\.\d+)', linea)
                airtime = re.search(r'Taire (\d+\.\d+)', linea)
                if tiempo and airtime:
                    tiempos.append(float(tiempo.group(1)))
                    airtimes_separados.append(float(airtime.group(1)))
            elif 'Tiempo en el aire de la agrupación (calculado con función):' in linea:
                agrupacion = re.search(r'(\d+\.\d+)', linea)
                if agrupacion:
                    airtime_agrupacion.append(float(agrupacion.group(1)))

    print("Tiempos:", tiempos)
    print("Airtimes separados:", airtimes_separados)
    print("Airtime agrupación:", airtime_agrupacion)
    
    return tiempos, airtimes_separados, airtime_agrupacion


def graficar(tiempos, airtimes_separados, airtime_agrupacion):
    fig, ax = plt.subplots()

    ax.plot(tiempos, airtimes_separados, label='Airtime sin agrupación', marker='o')
    
    # Crear una lista del mismo tamaño que 'tiempos' para airtime de agrupación
    airtime_agrupacion_full = [0] * len(tiempos)
    airtime_agrupacion_full[0] = airtime_agrupacion[0]  # Primer valor de agrupación
    airtime_agrupacion_full[len(tiempos)//2] = airtime_agrupacion[1]  # Segundo valor de agrupación

    ax.plot(tiempos, airtime_agrupacion_full, label='Airtime con agrupación', marker='x')

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Airtime')
    ax.set_title('Airtime ocupado con y sin agrupación')
    ax.legend()

    plt.show()

archivo = 'airtime.txt'  # Cambia esto por el nombre de tu archivo
tiempos, airtimes_separados, airtime_agrupacion = leer_datos(archivo)
graficar(tiempos, airtimes_separados, airtime_agrupacion)
