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
    #MSDUs = AMSDU_gen(ndatip, tdatip)
    
    # for i in range (paquete):
    #     print("MSDU:",i+1, MSDUs[i])
    #     print(hexdump(MSDUs[i].to_bytes((MSDUs[i].bit_length() + 7) // 8, byteorder='big')))
    (Hdr, mpduCi, ps, xs) = AMSDU_enc(paquete, ps, xs, Hdr) #para mas adelante, añadir las claves como parametros de entrada y quitarlos de la salida
    
    # print("Para transmitir",mpduCi)
    # print("Claves P",ps)
    # print("Claves S",xs)
    #mpduCi_Hex = mpduCi #.to_bytes((mpduCi.bit_length() + 7) // 8, byteorder='big')
    return (Hdr, mpduCi, ps, xs)



def AMSDU_gen (ndatip, longitud_payload):                      # Función para generar un Array con una cantidad de MSDUs determinados
                                                                          # de longitud determinada
    MSDUs = []
    for i in range (ndatip):                               # Lo construímos adjuntando cada MSDU
        MSDU = MSDU_gen(random.randint(longitud_payload,(longitud_payload+32)), 'true')
        MSDUs.append(MSDU)
    return (MSDUs)

def MSDU_gen (longitud_payload, no_ultimo):                                # Función para quenerar un MSDU de datos aleatorio, pero con cabeceras correctas
    DA =b'\x80\xc0\xca\xa4\x73\x11'                                # No sabemos a priori al valor de este campo, así que elgimos un valor aleatorio
    SA =b'\x80\xc0\xca\xa4\x73\x22'                                         # No sabemos a priori al valor de este campo, así que elgimos un valor aleatorio
    Payload = secrets.token_bytes(longitud_payload)                          # Elegimos una carga aleatoria de tamaño fijado en la entrada
    Imponible = DA + SA + longitud_payload.to_bytes(2, byteorder='big') + Payload

    longitud_padding = 4 - (len(Imponible)%4)                             # Calculamos la longitud del padding
    if ((longitud_padding != 4) and (no_ultimo == 'true')):
        MSDU = Imponible + secrets.token_bytes(longitud_padding)
        #print("MSDU con padding:")
        #print(hexdump(MSDU))                                                 #NO ES NECESARIO EL PADDING ESTE
    else: 
        MSDU = Imponible                                                 # Añadimos el padding si lo necesita
        #print("MSDU sin padding:")
        #print(hexdump(MSDU))

    a=int.from_bytes(MSDU, byteorder='big')
    return a

def AMSDU_enc(MSDU,ps,xs,Hdr):  # Función que cifra un AMSDU con el teorema chino del resto (CRT) - modificacion con poner un AMPDU
    MSDUs = []  # Creamos una lista para los MSDUs "desentramados"
    #ps = [179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137859,179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224138297,179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224139329]  # Claves p
    #xs = [61532612183151989766205930813815390561113443681681995968199490173335911003999835523462532284700903164815026579044079760856420774246591642260901445439556024314129223936683100465128572657093503929612010803385711998703274746779669296639247107519144430016244277254712761539919575437442485825044104359387159626929,120781863151076811603081594916227825651416067084458792888542504637690763567576631037593224201000755476707793103068861009762577113930453708881018257354997989329587724231518046518710393730889967935611457708286584393144022526743144545050205260685693388951693551689347099298998954185105522421238538460149080238638,161702939626961102214505275865271225206715896353268350766272671718496391264978431038625871186631352027387835432150896808568601625068134836123499346488984068808037198213510796804394267107018198782462497610069064651555240867118401607677903262347922945067400695320147133370330389756550130427661712676155559611346]  # Claves x
    psnew = []
    xsnew = []
    pnew = []
    a = []  # Máscaras aleatorias
    n = 0  # Contador de MSDUs
    #Hdr = 12314424523399710210377055948372200154747154392094740560503724206906022954002244618803685360758315659701276735008769000695511885412906532531089465728788755777024080035650333674571007093841665832408801892543453072679102516126499144572080316015256649831656764126714033757046360935953611148682454945422624310449049280714032644653811283481540567971641506162904269545062901200424985226375639476019497242470140928784573424919287449248685759321678318303711811796790211017166833329145702520802392138903041560116976916715063653113568534758725811860479016444823763434590746562056902647016766036466919171940638281511890168065335
    # print("HDR", Hdr)
    tiempo_inicial = datetime.now()
    for i in MSDU:
        # print("MSDU ANTES DE ENCRIPTAR",i)
        
        a.append((i + pow(Hdr, xs[n], ps[n])) % ps[n])  # y enmascaro el MSDU
        n = n + 1
        
        
    Payload = chinese_remainder(ps, a)
    longitud_payload = (7 + Payload.bit_length()) // 8                     # Calculamos la longitud en bytes del payload
    MPDU = Payload.to_bytes(longitud_payload, byteorder='big')

    return (Hdr, MPDU, ps, xs)




def AMSDU_dec_limpia(Hdr, MSDU, ps, xs):  # Función para descifrar una MSDU cifrado con CRT
    MSDUs = []  # Inicializamos la lista de salida
    
    for i in range(len(ps)):
        MSDUs.append((MSDU - pow(Hdr, xs[i], ps[i])) % ps[i])

    return (MSDUs)



def calcPRIMOS(num, long):
    newp = 2 ** long
    psnew = []
    xsnew = []
    pnew = []
    a = []  # Máscaras aleatorias
    n = 0  # Contador de MSDUs
    Hdr = random.getrandbits(2047)  # Cabecera común para el cifrado aleatorio
    m = 2 ** (long * 8)
    for i in list(range(num)):
        print("Entro en el bucle con m=", m)
        pnew = nextprime(m + 3)  # Calculo la clave p
        print("sigo en el bucle con i=", i)
        m = pnew
        psnew.append(pnew)  # y la almaceno en una lista
        xsnew.append(getrandbits(pnew.bit_length() - 1))  # Calculo la máscara aleatoria de cada diferente difrado
    print(pnew, psnew, xsnew)
    print("HDR", Hdr)
    return


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
