import subprocess

# ejecutar como root!!
# Interfaces que se quieren usar
interfaces = ['wlx00c0caa4737b', 'wlx00c0caa81a35']

for inter in interfaces:
    # Activar la interfaz
    subprocess.run(['ifconfig', inter, 'up'])

    # Configurar la interfaz en modo monitor
    subprocess.run(['iwconfig', inter, 'mode', 'monitor'])

    # Cambiar al canal 1 (2.412 GHz)
    subprocess.run(['iwconfig', inter, 'channel', '1'])

    # Mostrar la información de la interfaz después de la configuración
    info = subprocess.run(['iwconfig', inter], capture_output=True, text=True)
    print(f"Información de la interfaz {inter} después de la configuración:")
    print(info.stdout)
