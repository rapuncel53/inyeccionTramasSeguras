import subprocess

def listar_interfaces_wifi():
    try:
        resultado = subprocess.check_output(['iwconfig'], stderr=subprocess.STDOUT).decode('utf-8')
        lineaAnterior = ""
        interface_Managed = []
        interface_Monitor = []
        for line in resultado.split('\n'):
            if 'Managed' in line:
                interface_Managed.append(lineaAnterior.split()[0]) 
            if 'Monitor' in line:
                interface_Monitor.append(lineaAnterior.split()[0])     
            lineaAnterior = line
        return interface_Managed, interface_Monitor
            
    except subprocess.CalledProcessError as e:
        print("Error al listar interfaces WiFi:", e.output.decode())
        return [],[]

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

def configurar_modo_managed(interface):
    try:
         # Activar la interfaz
        subprocess.run(['ifconfig', interface, 'up'])

    # Configurar la interfaz en modo monitor
        subprocess.run(['iwconfig', interface, 'mode', 'managed'])

    # Cambiar al canal 1 (2.412 GHz)
        subprocess.run(['iwconfig', interface, 'channel', '1'])
        # subprocess.check_call(['sudo', 'ifconfig', interface, 'down'])
        # subprocess.check_output(['sudo', 'iwconfig', interface, 'mode', 'monitor'])
        # subprocess.check_call(['sudo', 'ifconfig', interface, 'up'])
        print(f"La interfaz {interface} está ahora en modo managed.")
    except subprocess.CalledProcessError as e:
        print(f"Error al configurar {interface} en modo managed:", e.output.decode())

def main():
    interfaces_Managed,interfaces_Monitor = listar_interfaces_wifi()
    if not interfaces_Managed and not interfaces_Monitor:
        print("No se encontraron interfaces WiFi.")
        return
    
    print("Interfaces WiFi encontradas:")
    for i, iface in enumerate(interfaces_Managed):
        print(f"{i+1}. {iface} (Managed)")
    for i, iface in enumerate(interfaces_Monitor):
        print(f"X. {iface} (Monitor)")

    try:
        seleccion = int(input("Seleccione la interfaz que desea configurar en modo monitor (número): ")) - 1
        if seleccion < 0 or seleccion >= len(interfaces_Managed):
            print("Selección no válida.")
            return
        configurar_modo_monitor(interfaces_Managed[seleccion])
    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número.")

if __name__ == "__main__":
    main()
