from random import getrandbits
import sys
from sympy import nextprime

def generateAndSaveKeys(num, lengths):
    for i in range(num):
        with open('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba3/generar claves/resultados'+str(i)+'.txt', 'w') as file:
            print("Archivo resultados"+str(i)+".txt creado, generando claves...")
    for length in lengths:
        #psnew = []
        #xsnew = []
        m = 2 ** (length * 8) 
        for i in range(num):
            pnew = nextprime(m + 3)
            m = pnew
            psnew=pnew
            xsnew=getrandbits(pnew.bit_length() - 1)
            with open('/home/proyecto/Documentos/pruebaInyeccion/inyeccionTramasSeguras/prueba3/generar claves/resultados'+str(i)+'.txt', 'a') as file:
                if length == 128:
                    pnew = nextprime(m + 3)
                    m = pnew
                    psnew1 = pnew
                    xsnew1 = getrandbits(pnew.bit_length() - 1)
                    file.write(f"Length: {length}\n")
                    file.write(f"psnew.1: {psnew1}\n")
                    file.write(f"xsnew.1: {xsnew1}\n")
                    file.write("\n")

                file.write(f"Length: {length}\n")
                file.write(f"psnew: {psnew}\n")
                file.write(f"xsnew: {xsnew}\n")
                file.write("\n")
    print("Terminado, resultados en la carpeta /generar claves (resultadosX.txt)")

num=3
lengths=[128,144,160,176,192,208,224,240,256,272,288,304,320,336,352,368,384,400,416,432,448,464,480,496,512]
#lengths=[128]

generateAndSaveKeys(num,lengths)     