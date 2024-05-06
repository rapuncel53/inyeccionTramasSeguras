import subprocess

# Función para listar las interfaces disponibles
def listar_interfaces():
    result = subprocess.run(['iwconfig'], capture_output=True, text=True)
    interfaces = []
    lines = result.stdout.split('\n')
    for line in lines:
        if 'IEEE 802.11' in line:
            interface = line.split()[0]
            interfaces.append(interface)
    return interfaces

# Función para configurar la interfaz con un canal específico
def configurar_interfaz(interfaz, canal):
    # Activar la interfaz
    subprocess.run(['ifconfig', interfaz, 'up'])
    print(f"Interfaz {interfaz} activada.")

    # Configurar la interfaz en modo monitor
    subprocess.run(['iw', 'dev', interfaz, 'set', 'type', 'monitor'])
    print(f"Interfaz {interfaz} configurada en modo monitor.")

    # Cambiar al canal deseado
    subprocess.run(['iw', 'dev', interfaz, 'set', 'channel', canal])
    print(f"Interfaz {interfaz} configurada en el canal {canal}.")

# Obtener e imprimir las interfaces disponibles
print("Interfaces disponibles:")
interfaces_disponibles = listar_interfaces()
for idx, interface in enumerate(interfaces_disponibles):
    print(f"{idx + 1}. {interface}")

# Solicitar al usuario que elija una interfaz
opcion = int(input("Elige una interfaz (ingresa el número): "))
if opcion <= 0 or opcion > len(interfaces_disponibles):
    print("Opción inválida. Saliendo del script.")
    exit()

interfaz_elegida = interfaces_disponibles[opcion - 1]

# Solicitar al usuario que ingrese el canal deseado
canal_deseado = input("Ingresa el número del canal que deseas (por ejemplo, 1 para 2.412 GHz): ")

# Configurar la interfaz con el canal deseado
configurar_interfaz(interfaz_elegida, canal_deseado)
