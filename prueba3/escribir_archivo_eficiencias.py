# Define un archivo común
nombre_archivo = "airtime.txt"

# Función para escribir en el archivo
def escribir_en_archivo(texto, nombre_archivo=nombre_archivo):
    with open(nombre_archivo, "a") as f:
        f.write(texto + "\n")


