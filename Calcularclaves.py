from random import getrandbits
import random
import sys
from sympy import nextprime


def calcPRIMOS(num,long):
    newp=2**long
    psnew=[]
    xsnew=[]
    pnew=[]
    a = []  # Máscaras aleatorias
    n = 0  # Contador de MSDUs
    Hdr = random.getrandbits(2047)  # Cabecera común para el cifrado aleatorio
    m=2**(long*8)
    for i in list(range(num)):
        #print ("Entro en el bucle con m=",m)
        pnew = nextprime(m + 3)  # Calculo la clave p
        #print ("sigo en el bucle con i=",i)
        m=pnew
        psnew.append(pnew)  # y la almaceno en una lista
        xsnew.append(getrandbits(pnew.bit_length() - 1))  # Calculo la máscara aleatoria de cada diferente difrado
    print ("pnew",pnew)
    print ("psnew",psnew)
    print ("xsnew",xsnew)
    print("HDR", Hdr)
    return

num=int(sys.argv[1])
long=int(sys.argv[2])
calcPRIMOS(num,long)