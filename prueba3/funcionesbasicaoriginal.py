# -*- coding: utf-8 -*-
from pickle5 import pickle
import math
import random
#import binascii
import functools
import secrets
import zlib
#import random
#import secrets
#import functools
from datetime import datetime, timedelta
from scapy.utils import hexdump
from datetime import datetime, timedelta
from random import getrandbits
from Crypto.Cipher import  AES
from sympy import *

# This Python file uses the following encoding: utf-8
import os, sys

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
        print ("Entro en el bucle con m=",m)
        pnew = nextprime(m + 3)  # Calculo la clave p
        print ("sigo en el bucle con i=",i)
        m=pnew
        psnew.append(pnew)  # y la almaceno en una lista
        xsnew.append(getrandbits(pnew.bit_length() - 1))  # Calculo la máscara aleatoria de cada diferente difrado
    print (pnew,psnew,xsnew)
    print("HDR", Hdr)
    return

def cifrarCRTbasica(paquete, ps, xs, Hdr):  # Funcion para el calculo de las simulaciones y almacenamiento de
    # resultados parciales, que no incluye los descifrados ni el cifrado completo de
    # nuestra propuesta
    
    # print(paquete)
    
    mpduCi= AMSDU_enc(paquete, ps, xs, Hdr) 
    
    # print("Para transmitir",mpduCi)
    # print("Claves P",ps)
    # print("Claves S",xs)
    #mpduCi_Hex = mpduCi #.to_bytes((mpduCi.bit_length() + 7) // 8, byteorder='big')
    return (mpduCi)


def AMSDU_enc(MSDU,ps,xs,Hdr):  # Función que cifra un AMSDU con el teorema chino del resto (CRT) - modificacion con poner un AMPDU
    
    a = []  # Máscaras aleatorias
    n = 0  # Contador de MSDUs
    
    for i in MSDU:
        # print("MSDU ANTES DE ENCRIPTAR",i)
        #print("i=",i)
        x = int.from_bytes(i, byteorder='big') #el dato esta en bytes y hay que meterlo como dato entero
        a.append((x + pow(Hdr, xs[n], ps[n])) % ps[n])  # y enmascaro el MSDU
        n = n + 1
        
        
    Payload = chinese_remainder(ps, a)
    longitud_payload = (7 + Payload.bit_length()) // 8                     # Calculamos la longitud en bytes del payload
    MPDU = Payload.to_bytes(longitud_payload, byteorder='big')

    return (MPDU)




def AMSDU_dec_limpia(Hdr, MSDU, ps, xs):  # Función para descifrar una MSDU cifrado con CRT
    MSDUs = []  # Inicializamos la lista de salida
    
    for i in range(len(ps)):
        MSDUs.append((MSDU - pow(Hdr, xs[i], ps[i])) % ps[i])

    return (MSDUs)



def chinese_remainder(n, a):  # Función para calcular el cifrado con el CRT
    sum = 0
    prod = functools.reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):  # Función para calcular el inverso multiplicativo modular
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
