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
                tiempo = float(re.search(r'Tiempo (\d+\.\d+(?:e[+-]?\d+)?)', linea).group(1))#leo tiempo paquete
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

                # print("comparamos", retardos_agrupacion_y_solitarios[-1],tiempos_lectura_agrupacion_y_solitarios[-1])
                # print("comparamos solitarios",retardos_solitarios[-1],tiempos_lectura_solitarios[-1])

                tiempo_recepcion_anterior = tiempo_recepcion
            elif 'Tiempo total en el aire de los paquetes por separado =' in linea:
                airtime_suma = float(re.search(r'= (\d+\.\d+)', linea).group(1))#leo airtime suma de todos los paquetes agrupables
                tiempo = float(re.search(r'agrupacion (\d+\.\d+)', linea).group(1))#leo tiempo agrupacion
                tiempos_lectura_agrupacion_y_solitarios.append(tiempo-tiempo1)
                #print("comparamos",tiempo,tiempo1)

            elif 'Tiempo en el aire de la' in linea:
                airtime_agrupacion = float(re.search(r'(\d+\.\d+)', linea).group(1))
                tiempo_recepcion = max(tiempo_recepcion_anterior,tiempos_lectura_agrupacion_y_solitarios[-1])+airtime_agrupacion
                
                #print("tiempo recepcion",tiempo_recepcion)
                for i in range(npaquetes):
                    retardos_agrupacion_y_solitarios.append(tiempo_recepcion-tiempos_lectura_paquetes_agrupables[-npaquetes+i])
                    #print("comparamos",tiempo_recepcion_anterior,tiempos_lectura_agrupacion_y_solitarios[-1],tiempo_recepcion-tiempos_lectura_paquetes_agrupables[-npaquetes+i])
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

def graficar(tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios,archivo):
    fig, ax = plt.subplots(figsize=(12, 6))
    
   

    # Graficar Airtime de cada paquete como barras
    #print(tiempos_lectura_paquetes_agrupables_y_solitarios[:500])
    ax.scatter(tiempos_lectura_paquetes_agrupables_y_solitarios, retardos_agrupacion_y_solitarios, label='retardo de envio paquetes agrupables', color='red', marker ="o")
    ax.scatter(tiempos_lectura_solitarios, retardos_solitarios, label='retardo de envio paquetes grandes ', color='blue', marker ="x")
   
    ax.set_xlabel('Tiempos de lectura (segundos)')
    ax.set_ylabel('retardos de envio (segundos)')
    ax.set_title('retardos de envio paquetes agrupando')
    ax.legend()

    plt.tight_layout()
    

    # Guardar la gráfica en un archivo
    dir = "C:\\Users\\julia\\OneDrive - unizar.es\\Cuarto Teleco\\TFG\\MEMORIA\\graficas\\plots por separado\\" + archivo + "_agrupando.jpg"
    plt.savefig(dir)  # Puedes cambiar la extensión y el nombre del archivo
    plt.show()
    #plt.close()  # Cierra la figura
    
for i in range(1, 9):
    archivo = 'airtime550_200_' + str(7+i)+'0'  # Cambia esto por el nombre de tu archivo
    archivo = 'airtime_Captura'
    print(archivo)
    #archivo = 'airtime150_100_100'  # Cambia esto por el nombre de tu archivo
    tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios = leer_datos(archivo+'.txt')

# Comprobar si se han leído correctamente los datos
# if tiempos_lectura_paquetes_agrupables_y_solitarios and retardos_agrupacion_y_solitarios and tiempos_lectura_solitarios and retardos_solitarios:
    graficar(tiempos_lectura_paquetes_agrupables_y_solitarios,  retardos_agrupacion_y_solitarios, tiempos_lectura_solitarios,retardos_solitarios,archivo)
# else:
#     print("Error al leer los datos del archivo.")
