# Calcular eficiencia de los paquetes enviados
#Calculo de la eficiencia normal
# 1709109735.28317 120 3
# 1709109735.297369 166 1
# 1709109735.298179 144 1
# 1709109735.299248 101 1
# 1709109735.302568 163 2
# 1709109735.302594 184 3
# 1709109735.314173 37 2
# 1709109735.31519 39 3
# 1709109735.315216 128 3
# 1709109735.316375 163 1

# EMPEZAMOS POR EJEMPLO CON 120 DE TAMAÑO
# al tamaño de cada paquete le quitamos 20 bytes que es el verdadero payload  = 100 bytes (generados aleatorios)
# se le añade la cabecera IP con scapy = 120 bytes
# tambien se añade la cabecera ethernet 14 bytes = 134 bytes

#134 bytes es el paquete completo con cabecera ethernet e IP

#para cada paquete se guarda solo su payload ethernet = 120 bytes
# al principio de cada paquete para enviar se le añade en 2 bytes su tamaño = 122 bytes
# se agrupan los paquetes segun su estacion destino hasta que se llega al maximo de paquetes para alguna estacion o se pasa el tiempo.
# se agrupan en un paquete de 128 bytes y otro de el tamaño que falte para los paquetes restantes
# dentro del primer paquete de 128 se pone un byte para que empiece por 1 y se añade el tamaño de la contraseña del siguiente paquete 
# en dos bytes, por lo tanto se añaden 3 bytes de cabecera.
# en el segundo paquete si hay, se añade solamente el byte para que empiece por 1.
# osea que se añaden 3 bytes de cabecera fijos en el primer paquete, 1 byte mas si hay mas paquetes para la misma estacion destino
# y 2 bytes extra por cada paquete que este en la agrupacion.

#trama mac wifi
# 2 oct control + 2 oct duracion ID + 6 oct MAC1 + 6 oct MAC2 + 6 oct MAC3 +2 oct control + DATOS + 4 oct FCS

# DIFS y SIFS

# import sys
# import os

# # Añadir la carpeta que contiene el módulo a sys.path
# sys.path.append(os.path.abspath("/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba3"))

# # Ahora puedes importar el módulo
# from a_generarFicheroPaquetes import leer_datos_paquetes



#Cálculo del tiempo que tarda en mandar un paquete de longitud L
#  Estimación SIN envío de RTS/CTS:
L = 2 #(tamaño datos)
Rb = 11
DIFS = 50 * 10**(-6)
Backoff_medio = 310 * 10**(-6)
TDataPreambulo = TAckPreambulo = 96 * 10**(-6)
TDataMac = (L+36)*8/Rb
SIFS = 10 * 10**(-6)
TAckMac = 14*8/Rb
Tpaquete = DIFS + Backoff_medio + TDataPreambulo +TDataMac + SIFS + TAckPreambulo + TAckMac

def calcularEficiencia(nombre_archivo):

    TTotal = 0
    i=0
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines() #leemos las lineas del archivo
            
            for linea in lineas:
                
                # Dividir la línea en tiempo, tamaño y destino
                tiempo, tamano, destino = linea.strip().split(' ')
                L = int(tamano)
                TDataMac = (L+36)*8/Rb
                Tpaquete = DIFS + Backoff_medio + TDataPreambulo +TDataMac + SIFS + TAckPreambulo + TAckMac
                print("Tiempo paquete ",i," = ",Tpaquete)
                TTotal += Tpaquete
                i += 1
            print("Tiempo total en el aire de los paquetes por separado = ", TTotal)




    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
    except ValueError:
        print("Error al convertir el tiempo a entero.")

# eth_paquetes = leer_datos_paquetes("/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba3/datosPaquetes2.txt")
# for paquetes in eth_paquetes:
#     print("paquetes")


#calcularEficiencia("/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba3/datosPaquetes.txt")



# Parámetros para Diferentes Protocolos
# 802.11b
# Velocidad de Transmisión (Rb): 1, 2, 5.5, 11 Mbps (usaremos 11 Mbps)
# DIFS: 50 µs
# SIFS: 10 µs
# Preambulo: 192 µs (long preamble), 96 µs (short preamble)
# ACK: 112 bits (14 bytes)