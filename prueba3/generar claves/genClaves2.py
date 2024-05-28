from random import getrandbits
import sys
from sympy import nextprime

def generateAndSaveKeys(num, lengths):
    print("generando...")
    with open('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba3/generar claves/resultados.txt', 'w') as file:
        for length in lengths:
            psnew = []
            xsnew = []
            m = 2 ** (length * 8)
            for i in range(num):
                pnew = nextprime(m + 3)
                m = pnew
                psnew.append(pnew)
                xsnew.append(getrandbits(pnew.bit_length() - 1))
            file.write(f"Length: {length}\n")
            file.write(f"psnew: {psnew}\n")
            file.write(f"xsnew: {xsnew}\n")
            file.write("\n")
    print("Terminado, resultados en la carpeta /generar claves")

num=1
lengths=[128,144,160,176,192,208,224,240,256,272,288,304,320,336,352,368,384,400,416,432,448,464,480,496,512]
lengths=[128]

generateAndSaveKeys(num,lengths)     