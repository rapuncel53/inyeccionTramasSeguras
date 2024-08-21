def claves(mac, tamaño):
    """
    Obtiene las claves ps y xs correspondientes a una dirección MAC y tamaño de paquete.

    Argumentos:
    - mac: Dirección MAC como string.
    - tamaño: Tamaño del paquete como entero.

    Retorna:
    - claveps: Clave ps obtenida del archivo.
    - clavexs: Clave xs obtenida del archivo.
    """
    archivo = f"/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba6/claves/{mac}.txt"
    claveps = None
    clavexs = None

    # Diccionario que mapea rangos de tamaño a líneas en el archivo
    rangos_tamano = {
        -1: (1, 2),
        128: (5, 6),
        144: (9, 10),
        160: (13, 14),
        176: (17, 18),
        192: (21, 22),
        208: (25, 26),
        224: (29, 30),
        240: (33, 34),
        256: (37, 38),
        272: (41, 42),
        288: (45, 46),
        304: (49, 50),
        320: (53, 54),
        336: (57, 58),
        352: (61, 62),
        368: (65, 66),
        384: (69, 70),
        400: (73, 74),
        416: (77, 78),
        432: (81, 82),
        448: (85, 86),
        464: (89, 90),
        480: (93, 94),
        496: (97, 98),
        512: (101, 102)
    }

    with open(archivo, "r") as file:
        lines = file.readlines()
        for limite, (ps_idx, xs_idx) in sorted(rangos_tamano.items()):
            if tamaño <= limite:
                claveps = int(lines[ps_idx].split(": ")[1].strip())
                clavexs = int(lines[xs_idx].split(": ")[1].strip())
                break

    return claveps, clavexs

# Ejemplo de uso:
# claveps, clavexs = claves("11:11:11:11:11:11", 123)
# print(claveps, clavexs)
