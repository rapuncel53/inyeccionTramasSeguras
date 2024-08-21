import subprocess

def listar_interfaces_wifi():
    try:
        resultado = subprocess.check_output(['iwconfig'], stderr=subprocess.STDOUT).decode('utf-8')
        lineaAnterior = ""
        interface = []
        for line in resultado.split('\n'):
            if 'Managed' in line:
                interface.append(lineaAnterior.split()[0]) 
                
            lineaAnterior = line
        return interface
            
    except subprocess.CalledProcessError as e:
        print("Error al listar interfaces WiFi:", e.output.decode())
        return []

def configurar_modo_monitor(interface):
    try:
         # Activar la interfaz
        subprocess.run(['ifconfig', interface, 'up'])

    # Configurar la interfaz en modo monitor
        subprocess.run(['iwconfig', interface, 'mode', 'monitor'])

    # Cambiar al canal 1 (2.412 GHz)
        subprocess.run(['iwconfig', interface, 'channel', '1'])
        # subprocess.check_call(['sudo', 'ifconfig', interface, 'down'])
        # subprocess.check_output(['sudo', 'iwconfig', interface, 'mode', 'monitor'])
        # subprocess.check_call(['sudo', 'ifconfig', interface, 'up'])
        print(f"La interfaz {interface} está ahora en modo monitor.")
    except subprocess.CalledProcessError as e:
        print(f"Error al configurar {interface} en modo monitor:", e.output.decode())

def main():
    interfaces = listar_interfaces_wifi()
    if not interfaces:
        print("No se encontraron interfaces WiFi.")
        return
    
    print("Interfaces WiFi encontradas:")
    for i, iface in enumerate(interfaces):
        print(f"{i+1}. {iface}")

    try:
        seleccion = int(input("Seleccione la interfaz que desea configurar en modo monitor (número): ")) - 1
        if seleccion < 0 or seleccion >= len(interfaces):
            print("Selección no válida.")
            return
        configurar_modo_monitor(interfaces[seleccion])
    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número.")

if __name__ == "__main__":
    main()