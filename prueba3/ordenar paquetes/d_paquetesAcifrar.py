from e_calcularClaves import *
from a_generarFicheroPaquetes import leer_datos_paquetes
from b_ordenarpaquetes import ordenarpaquetes
from c_colocarCabeceras import colocarcabeceras
primer_llamado = True  # Bandera para controlar la primera llamada
def paquetesacifrar(paquetes_con_cabeceras):  #ASIGNA LAS CLAVES A CADA PAQUETE
    
    paquetes_a_cifrar = []
    xs = []
    ps = []
    Hdr = 2843796326746969865517775137331587486046904811886503323102856146256129856445998934622446266251760018784185737111736108364839797946641759100223128000616308091539303132799727619266259596828149083874517781740179944644935556803289876169647362898861310839047877703563616025850495911850867054594022211735083536843875628987627216327719706741910036986827677832845686557780528840150455730953809234694322995111692138428714417268185133762942049850455209445920069601946607745983683598930918306972219800721120122707225650964714727753960963676306745813930269021935324632162446815277154321124916795985950915416767654347652388677539 #

    for mac in paquetes_con_cabeceras:
        primer_llamado = True  # Bandera para controlar la primera llamada
        for paquete in paquetes_con_cabeceras[mac]:
            
            paquetes_a_cifrar.append(paquete)
            # print("mac")
            # print(mac)
            # print("lenpaquete")
            # print (len(paquete))
            if primer_llamado:
                ps1,xs1 = claves1(mac, len(paquete))
                ps.append(ps1)
                xs.append(xs1)
            else:
                ps2,xs2 = claves2(mac, len(paquete))
                ps.append(ps2)
                xs.append(xs2)
            primer_llamado = False  # Después de la primera llamada, cambiar la bandera
                                                                                                                                      
    return paquetes_a_cifrar,ps,xs,Hdr #paquete y claves

eth_paquetes = leer_datos_paquetes("datosPaquetes.txt")
for paquetes in eth_paquetes:
    ord_paquetes = ordenarpaquetes(paquetes) #aqui no se pierde paquetes
    cab_paquetes = colocarcabeceras(ord_paquetes)
    cif_paquetes = paquetesacifrar(cab_paquetes)
    tamañocifrar = 0
    for paquete in cif_paquetes[0]:
        tamañocifrar += len(paquete)
    print ("tamaño total a cifrar",tamañocifrar)
    