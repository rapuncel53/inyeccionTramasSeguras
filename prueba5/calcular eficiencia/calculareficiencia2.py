def calculate_airtime(protocol, Rb, L=1386):
    if protocol == '802.11b':
        DIFS = 50 * 10**-6
        SIFS = 10 * 10**-6
        Backoff_medio = 310 * 10**-6
        Preambulo = 96 * 10**-6
    elif protocol == '802.11g':
        DIFS = 34 * 10**-6
        SIFS = 16 * 10**-6
        Backoff_medio = 310 * 10**-6
        Preambulo = 20 * 10**-6
    elif protocol == '802.11n':
        DIFS = 34 * 10**-6
        SIFS = 10 * 10**-6
        Backoff_medio = 310 * 10**-6
        Preambulo = 40 * 10**-6
    elif protocol == '802.11ac':
        DIFS = 34 * 10**-6
        SIFS = 16 * 10**-6
        Backoff_medio = 310 * 10**-6
        Preambulo = 20 * 10**-6
    elif protocol == '802.11ax':
        DIFS = 34 * 10**-6
        SIFS = 16 * 10**-6
        Backoff_medio = 310 * 10**-6
        Preambulo = 20 * 10**-6
    else:
        raise ValueError("Protocolo no soportado")
    
    TDataMac = (L + 36) * 8 / Rb
    TAckMac = 14 * 8 / Rb
    
    Tpaquete = DIFS + Backoff_medio + Preambulo + TDataMac + SIFS + Preambulo + TAckMac
    #print("Valores2 : ",DIFS,Backoff_medio,Preambulo,TDataMac,SIFS,Preambulo,TAckMac)
    
    return Tpaquete

def main():
    protocols = {
        1: {'name': '802.11b', 'rates': [1, 2, 5.5, 11]},
        2: {'name': '802.11g', 'rates': [6, 9, 12, 18, 24, 36, 48, 54]},
        3: {'name': '802.11n', 'rates': [6.5, 13, 19.5, 26, 39, 52, 58.5, 65, 78, 104, 117, 130, 156, 195, 208, 234, 260, 312, 390, 520, 600]},
        4: {'name': '802.11ac', 'rates': [7.2, 14.4, 21.7, 28.9, 43.3, 57.8, 65, 86.7, 115.6, 130, 173.3, 200, 216.7, 234, 260, 293.3, 400, 433.3, 520, 600, 650, 800, 866.7, 1000, 1050, 1200, 1300, 1400, 1600, 1733.3, 1950, 2000, 2100, 2400, 2600, 2800, 2933.3, 3000, 3466.7, 3900, 4333.3, 4550, 5200, 5850, 6500, 6933.3]},
        5: {'name': '802.11ax', 'rates': [3.6, 7.2, 10.8, 14.4, 21.6, 28.8, 43.2, 57.6, 65, 86.4, 108, 129.6, 144, 172.8, 216, 240, 259.2, 288, 345.6, 360, 432, 480, 540, 576, 600, 648, 720, 800, 864, 900, 960, 1080, 1200, 1296, 1440, 1560, 1728, 1800, 1920, 2160, 2400, 2592, 2880, 3120, 3240, 3456, 3600, 3840, 4000, 4320, 4800, 5160, 5400, 5760, 6000, 6480, 7200, 7680, 8000, 8640, 9216, 9600, 10080]}
    }

    print("Seleccione el protocolo WiFi:")
    for key, value in protocols.items():
        print(f"{key}. {value['name']}")
    
    option = int(input("Ingrese el número del protocolo: "))
    if option not in protocols:
        print("Opción no válida")
        return
    
    protocol = protocols[option]['name']
    rates = protocols[option]['rates']
    
    print(f"Seleccione la velocidad de transmisión para {protocol} (Mbps):")
    for idx, rate in enumerate(rates, start=1):
        print(f"{idx}. {rate}")

    rate_option = int(input("Ingrese el número de la velocidad: "))
    if rate_option < 1 or rate_option > len(rates):
        print("Opción no válida")
        return

    Rb = rates[rate_option - 1] * 10**6  # Convertir a bps

    nombre_archivo = "/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba3/datosPaquetes2.txt"
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            i = 1
            for linea in lineas:
                
                # Dividir la línea en tiempo, tamaño y destino
                tiempo, tamano, destino = linea.strip().split(' ')
                
     
                tamano = int(tamano)
                
                airtime = calculate_airtime(protocol, Rb, tamano)
                print(f"El tiempo en el aire para el paquete {i} con el protocolo {protocol} y una velocidad de {Rb / 10**6} Mbps es {airtime * 10**3:.3f} ms")
                i+=1
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
    except ValueError:
        print("Error al convertir el tiempo a entero.")
if __name__ == "__main__":
    main()
