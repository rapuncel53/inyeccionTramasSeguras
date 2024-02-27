# -*- coding: utf-8 -*-
from pickle5 import pickle
import math
import random
#import binascii
import functools
import secrets
import zlib
import random
import secrets
import functools
from datetime import datetime, timedelta
from scapy.utils import hexdump
from datetime import datetime, timedelta
from random import getrandbits
from Crypto.Cipher import  AES
from sympy import *



# This Python file uses the following encoding: utf-8
import os, sys

def cifrarCRTclean():  # Funcion paara el calculo de las simulaciones y almacenamiento de
# resultados parciales, que no incluye los descifrados ni el cifrado completo de
# nuestra propuesta

    AMSDU, MSDUs = AMSDU_gen(3, 80)
    print("AMSDUs 1:  ", MSDUs[0])
    print(hexdump(MSDUs[0].to_bytes((MSDUs[0].bit_length() + 7) // 8, byteorder='big')))
    print("AMSDUs 2:  ", MSDUs[1])
    print(hexdump(MSDUs[1].to_bytes((MSDUs[1].bit_length() + 7) // 8, byteorder='big')))
    print("AMSDUs 3:  ", MSDUs[2])
    print(hexdump(MSDUs[2].to_bytes((MSDUs[2].bit_length() + 7) // 8, byteorder='big')))

    (Hdr, mpduCi, ps, xs) = AMSDU_enc(AMSDU, MSDUs)
    # print("Para transmitir",mpduCi)
    # print("Claves P",ps)
    # print("Claves S",xs)
    mpduCi_Hex = mpduCi.to_bytes((mpduCi.bit_length() + 7) // 8, byteorder='big')
    return (Hdr, mpduCi_Hex, mpduCi, ps, xs)



def AMSDU_gen (longitud_agregado, longitud_payload):                      # Función para generar un AMSDU con una cantidad de MSDUs determinados
                                                                          # de longitud determinada
    AMSDU = 0                                                             # Inicializacion del AMSDU
    MSDUs = []
    filtro1 = (1 << 112)- 1                                               # Filtros para leer los campos de la cabecera
    filtro2 = (1 << 16) - 1
    for i in range (longitud_agregado - 1):                               # Lo construímos adjuntando cada MSDU
        MSDU = MSDU_gen_unos(i,random.randint(longitud_payload,(longitud_payload+32)))
        bytes_resultantes = (7 + MSDU.bit_length()) // 8
        cabecera = (MSDU & (filtro1 << (8 * (bytes_resultantes - 14)))) >> (8 * (bytes_resultantes - 14))
                                                                          # Calculamos la cabecera
        longitud = cabecera & filtro2                                     # Y la longitud del MSDU
        pad = 4 - (longitud % 4)
        if pad == 4: pad = 0
        MSDUs.append(MSDU)
        AMSDU = (AMSDU << (8 * bytes_resultantes)) ^ MSDU
    MSDU = MSDU_gen_unos(0,random.randint(longitud_payload,(longitud_payload+32)))                            # El ultimo MSDU sin padding
    MSDUs.append(MSDU)
    AMSDU = (AMSDU << (8 * ((7 + MSDU.bit_length()) // 8))) ^ MSDU
    return (AMSDU, MSDUs)


def MSDU_gen_unos(num_ultimos_4, longitud_MSDU):
    if not 0 <= num_ultimos_4 <= 15:
        raise ValueError("Los últimos 4 bits deben estar en el rango de 0 a 15")

    if longitud_MSDU < 2:
        raise ValueError("La longitud del MSDU debe ser al menos 2 para incluir la cabecera")

    if longitud_MSDU > 65535:
        raise ValueError("La longitud del MSDU excede el límite máximo de 65535 bytes")

    DA = b'\xFF\xFF\xFF\xFF\xFF\xFF'  # Dirección MAC del destinatario, todos los bytes en 1
    SA = b'\xFF\xFF\xFF\xFF\xFF\xFF'  # Dirección MAC del remitente, todos los bytes en 1
    payload_length = longitud_MSDU - 14  # Restamos la longitud de las direcciones MAC y la cabecera
    payload = b'\xFF' * (payload_length - 1)  # Datos de usuario, todos los bytes en 1 excepto 1 byte
    payload += num_ultimos_4.to_bytes(1, byteorder='big')  # Últimos 4 bits como el número proporcionado

    # Construimos el MSDU concatenando todos los campos
    MSDU = DA + SA + longitud_MSDU.to_bytes(2, byteorder='big') + payload
    a=int.from_bytes(MSDU, byteorder='big')
    print("MSDU:", MSDU.hex())
    return a


def AMSDU_enc(AMSDU,
              MSDU):  # Función que cifra un AMSDU con el teorema chino del resto (CRT) - modificacion con poner un AMPDU
    MSDUs = []  # Creamos una lista para los MSDUs "desentramados"
    # ps = [1100645304239144332874899719259313845702512851699,1100645304239144332874899719259330726252929972829,18465764008605840127818093568353291822549225699331595729]  # Claves p
    # xs = [469185440907188674086266365887713402920751416175,469185440907188674086266365887713402920751416175,7016009363412435780763082007262025939147461935248010908]  # Claves x
    ps = [
        179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137859,
        179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224138297,
        179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224139329]  # Claves p
    xs = [
        61532612183151989766205930813815390561113443681681995968199490173335911003999835523462532284700903164815026579044079760856420774246591642260901445439556024314129223936683100465128572657093503929612010803385711998703274746779669296639247107519144430016244277254712761539919575437442485825044104359387159626929,
        120781863151076811603081594916227825651416067084458792888542504637690763567576631037593224201000755476707793103068861009762577113930453708881018257354997989329587724231518046518710393730889967935611457708286584393144022526743144545050205260685693388951693551689347099298998954185105522421238538460149080238638,
        161702939626961102214505275865271225206715896353268350766272671718496391264978431038625871186631352027387835432150896808568601625068134836123499346488984068808037198213510796804394267107018198782462497610069064651555240867118401607677903262347922945067400695320147133370330389756550130427661712676155559611346]  # Claves x
    psnew = []
    xsnew = []
    pnew = []
    a = []  # Máscaras aleatorias
    n = 0  # Contador de MSDUs
    # Hdr = random.getrandbits(2047)  # Cabecera común para el cifrado aleatorio
    # Hdr=159543976004846760804451445532235299926780139435372300692241210008556993030617775319810894062225108814210887527046880361472530827326578978621918950536316748567721283223912773493214154863018969779796561231280601263793302777253129776032382760813815413222441888256216530367314241202928278526289479100743111536202
    Hdr = 12314424523399710210377055948372200154747154392094740560503724206906022954002244618803685360758315659701276735008769000695511885412906532531089465728788755777024080035650333674571007093841665832408801892543453072679102516126499144572080316015256649831656764126714033757046360935953611148682454945422624310449049280714032644653811283481540567971641506162904269545062901200424985226375639476019497242470140928784573424919287449248685759321678318303711811796790211017166833329145702520802392138903041560116976916715063653113568534758725811860479016444823763434590746562056902647016766036466919171940638281511890168065335
    # print("HDR", Hdr)
    filtro1 = (1 << 112) - 1  # Filtros para leer los campos de la cabecera
    filtro2 = (1 << 16) - 1
    tiempo_inicial = datetime.now()
    m = 2
    for i in MSDU:
        # print("MSDU ANTES DE ENCRIPTAR",i)
        # pnew = nextprime(m*i + 3)  # Calculo la clave p
        m = m * 2
        # psnew.append(pnew)  # y la almaceno en una lista
        # xsnew.append(getrandbits(pnew.bit_length() - 1))  # Calculo la máscara aleatoria de cada diferente difrado
        a.append((i + pow(Hdr, xs[n], ps[n])) % ps[n])  # y enmascaro el MSDU
        n = n + 1
    # print (pnew,psnew,xsnew)

    return (Hdr, MPDU_gen(MSDU_gen2(chinese_remainder(ps, a))), ps,
            xs)  # Devuelvo la cabecera aleatoria y un MPDU cifrado con el CRT


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
