# -*- coding: utf-8 -*-
import random
import functools
from sympy import nextprime

def calcPRIMOS(num, long):
    """
    Calcula números primos y sus correspondientes máscaras aleatorias.

    Parameters:
        num (int): Número de primos a calcular.
        long (int): Longitud de los primos.

    Returns:
        tuple: Tupla con la última clave prima generada y las listas de primos y máscaras aleatorias.
    """
    m = 2**(long * 8)
    psnew = []
    xsnew = []
    pnew = None
    Hdr = random.getrandbits(2047)

    for _ in range(num):
        pnew = nextprime(m + 3)
        m = pnew
        psnew.append(pnew)
        xsnew.append(random.getrandbits(pnew.bit_length() - 1))

    return pnew, psnew, xsnew, Hdr

def cifrarCRTbasica(paquete, ps, xs, Hdr):
    """
    Realiza la simulación del cifrado CRT básico.

    Parameters:
        paquete (bytes): Datos a cifrar.
        ps (list): Lista de primos.
        xs (list): Lista de máscaras aleatorias.
        Hdr (int): Cabecera para el cifrado.

    Returns:
        bytes: Datos cifrados.
    """
    mpduCi = AMSDU_enc(paquete, ps, xs, Hdr)
    return mpduCi

def AMSDU_enc(MSDU, ps, xs, Hdr):
    """
    Cifra un AMSDU con el teorema chino del resto (CRT).

    Parameters:
        MSDU (bytes): Datos a cifrar.
        ps (list): Lista de primos.
        xs (list): Lista de máscaras aleatorias.
        Hdr (int): Cabecera para el cifrado.

    Returns:
        bytes: Datos cifrados.
    """
    a = []
    n = 0

    for i in MSDU:
        x = int.from_bytes(i, byteorder='big')
        a.append((x + pow(Hdr, xs[n], ps[n])) % ps[n])
        n += 1

    Payload = chinese_remainder(ps, a)
    longitud_payload = (7 + Payload.bit_length()) // 8
    MPDU = Payload.to_bytes(longitud_payload, byteorder='big')

    return MPDU

def AMSDU_dec_limpia(Hdr, MSDU, ps, xs):
    """
    Descifra una MSDU cifrada con CRT.

    Parameters:
        Hdr (int): Cabecera para el cifrado.
        MSDU (bytes): Datos cifrados.
        ps (list): Lista de primos.
        xs (list): Lista de máscaras aleatorias.

    Returns:
        list: Lista de datos descifrados.
    """
    MSDUs = []

    for i in range(len(ps)):
        MSDUs.append((MSDU - pow(Hdr, xs[i], ps[i])) % ps[i])

    return MSDUs

def chinese_remainder(n, a):
    """
    Calcula el cifrado con el Teorema Chino del Resto (CRT).

    Parameters:
        n (list): Lista de primos.
        a (list): Lista de máscaras aleatorias.

    Returns:
        int: Resultado del cifrado.
    """
    sum = 0
    prod = functools.reduce(lambda a, b: a * b, n)

    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p

    return sum % prod

def mul_inv(a, b):
    """
    Calcula el inverso multiplicativo modular.

    Parameters:
        a (int): Número.
        b (int): Módulo.

    Returns:
        int: Inverso multiplicativo modular.
    """
    b0 = b
    x0, x1 = 0, 1

    if b == 1:
        return 1

    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0

    if x1 < 0:
        x1 += b0

    return x1
