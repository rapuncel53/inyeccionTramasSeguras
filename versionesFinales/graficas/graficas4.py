import matplotlib.pyplot as plt
import re

def leer_datos(archivo):
    tiempos = []
    airtimes_separados = []
    airtimes_datagramas_suma = []
    airtimes_agrupaciones = []
    tiempos_T_agrupaciones = []
    retardo_con_agrupaciones = []
    tiempo1=None
    npaquetes=0 
    with open(archivo, 'r') as file:
        
        for linea in file:
            if 'paquete numero' in linea:
                npaquetes+=1#cuento los paquetes
                tiempo = float(re.search(r'Tiempo (\d+\.\d+)', linea).group(1))#leo tiempo paquete
                airtime = float(re.search(r'Taire (\d+\.\d+)', linea).group(1))#leo airtime paquete
                
                if tiempo1==None:
                    tiempo1=tiempo
                tiempos.append(tiempo-tiempo1)#guardo los tiempos referenciados al primer paquete
                airtimes_separados.append(airtime)#guardo los airtime de cada paquete
            elif 'Tiempo total en el aire de los paquetes por separado =' in linea:
                tiempo_total_separado = float(re.search(r'(\d+\.\d+)', linea).group(1))
                airtimes_datagramas_suma.append(tiempo_total_separado)
                tiempos_T_agrupaciones.append(tiempos[-1])
            elif 'Tiempo en el aire de la' in linea:
                tiempo_agrupado = float(re.search(r'(\d+\.\d+)', linea).group(1))
                airtimes_agrupaciones.append(tiempo_agrupado)
                for i in range(npaquetes):
                    retardo_con_agrupaciones.append(tiempos_T_agrupaciones[-1]+airtimes_agrupaciones[-1]-tiempos[-npaquetes+i]) #  retardo_con_agrupaciones
                    # print("envio agrupacion",tiempos_T_agrupaciones[-1])
                    # print("airtime agrupacion",airtimes_agrupaciones[-1])
                    # print("leo paquete",tiempos[-i])
                    # print("llega paquete",retardo_con_agrupaciones[-1])
                npaquetes=0

    
    print("tiempos", tiempos, " airtimes_separados", airtimes_separados[0], 
          " airtimes_datagramas_suma", airtimes_datagramas_suma[0], 
          " airtimes_agrupaciones", airtimes_agrupaciones[0])
    
    return tiempos, airtimes_separados, airtimes_datagramas_suma, airtimes_agrupaciones, tiempos_T_agrupaciones, retardo_con_agrupaciones

def graficar(tiempos, airtimes_separados, airtimes_datagramas_suma, airtimes_agrupaciones, tiempos_T_agrupaciones, retardo_con_agrupaciones):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    #tiempos empezando en 0
    tiempos_envio_desde_0=[0]
    for i in range(len(tiempos)-1):
        Tenvio_anterior=tiempos[i]+airtimes_separados[0]
        tiempos_envio_desde_0.append(max(Tenvio_anterior,tiempos[i+1]))

     
    #tiempos de envio sin superponerse
    tiempos_envio_reales_individuales=[0]
    for i in range(len(tiempos)-1):
        Tenvio_anterior=tiempos_envio_reales_individuales[i]+airtimes_separados[i]
        tiempos_envio_reales_individuales.append(max(Tenvio_anterior,tiempos[i+1]))

    # tiempos_envio_reales_suma=[tiempos_T_agrupaciones[0]]
    # for i in range(len(tiempos_T_agrupaciones)-1):
    #     Tenvio_anterior=tiempos_envio_reales_suma[i]+airtimes_datagramas_suma[i]
    #     tiempos_envio_reales_suma.append(max(Tenvio_anterior,tiempos_T_agrupaciones[i+1]))

    tiempos_envio_reales_agrupacion=[tiempos_T_agrupaciones[0]]
    for i in range(len(tiempos_T_agrupaciones)-1):
        Tenvio_anterior=tiempos_envio_reales_agrupacion[i]+airtimes_agrupaciones[i]
        tiempos_envio_reales_agrupacion.append(max(Tenvio_anterior,tiempos_T_agrupaciones[i+1]))

    retardo_de_envio_individuales= []
    for i in range (len(tiempos)):
        retardo_de_envio_individuales.append(tiempos_envio_reales_individuales[i]+airtimes_separados[i]-tiempos_envio_desde_0[i])

    # retardo_de_envio_agrupaciones= []
    # for i in range (len(tiempos)):
    #     retardo_de_envio_agrupaciones.append(tiempos_envio_reales_agrupacion[i]+airtimes_agrupaciones[i]-tiempos_envio_reales_agrupacion[i])


    # Graficar Airtime de cada paquete como barras
    ax.plot(tiempos_envio_desde_0, retardo_de_envio_individuales, label='retardo de envio individuales', color='red', marker ="o")
    print("tiempos ",len(tiempos))
    
    ax.plot(tiempos, retardo_con_agrupaciones, label='retardo de envio agrupaciones', color='blue', marker ="o")
    #print("tiempos ",len(tiempos))
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('retardos de envio')
    ax.set_title('retardos de envio agrupando y sin agrupar')
    ax.legend()

    plt.tight_layout()
    plt.show()

    # Guardar la gráfica en un archivo
    plt.savefig('rayleigh_distribution_mean_0.0005.png')  # Puedes cambiar la extensión y el nombre del archivo
    plt.close()  # Cierra la figura
    

archivo = 'airtime8(raileigM0.0007).txt'  # Cambia esto por el nombre de tu archivo
tiempos, airtimes_separados, airtimes_datagramas_suma, airtimes_agrupaciones, tiempos_T_agrupaciones, retardo_con_agrupaciones = leer_datos(archivo)

# Comprobar si se han leído correctamente los datos
if tiempos and airtimes_separados and airtimes_datagramas_suma and airtimes_agrupaciones:
    graficar(tiempos, airtimes_separados, airtimes_datagramas_suma, airtimes_agrupaciones, tiempos_T_agrupaciones, retardo_con_agrupaciones)
else:
    print("Error al leer los datos del archivo.")
