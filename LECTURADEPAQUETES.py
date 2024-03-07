from scapy.all import rdpcap

def leer_paquetes_pcap(archivo_pcap):
    paquetes = []  # Lista con los paquetes leídos del pcap
    macdst = {}    # Diccionario con las MAC detectadas y los payloads

    # Mapeo de índices a direcciones MAC
    mac_mappings = {
        1: "11:11:11:11:11:11",
        2: "11:11:11:11:11:11",
        3: "11:11:11:11:11:11",
        4: "22:22:22:22:22:22",
        5: "22:22:22:22:22:22",
        6: "22:22:22:22:22:22",
        7: "33:33:33:33:33:33",
        8: "33:33:33:33:33:33",
        9: "33:33:33:33:33:33",
        10: "33:33:33:33:33:33"
    }

    # Leer el archivo .pcap
    try:
        print("intentando leer pcap")

        packets = rdpcap(archivo_pcap)  # Lee del archivo
    except FileNotFoundError as e:
        # Captura la excepción y obtén el mensaje de error
        mensaje_error = str(e)
        
        print("El archivo .pcap no fue encontrado."+ mensaje_error)
        return [], {}

    for i, pkt in enumerate(packets):
        mac = mac_mappings.get(i + 1)  # Los índices comienzan en 1
        if mac:
            if mac not in macdst:    # si se encuentra una mac nueva
                macdst[mac] = []          # Se crea un array con la mac como nombre
            macdst[mac].append(bytes(pkt.payload).hex())  # se almacenan los paquetes con esa mac destino

        # Si necesitas los datos de los paquetes también los puedes almacenar en paquetes
        paquetes.append(pkt)

    return paquetes, macdst



# Nombre del archivo .pcap
#archivo_pcap = "paquetes prueba.pcap"  # Cambiar por la ruta correcta de tu archivo

# Llamar a la función para leer el archivo .pcap y obtener los paquetes
#paquetes, ampdu = leer_paquetes_pcap(archivo_pcap)

print(ampdu)



# Ahora tenemos un array parecido a este {mac : payloads en hexadecimal uno detras del otro}
#{'11:11:11:11:11:11': ['450000280f77400080060000c0a801b70215b4def1ba01bb0d90699c89dea83250110204796d0000', '4500002827eb400080060000c0a801b75c7b2183f1bc01bb53ec900bd15c26e65011020440780000', '45000028f4b4400080060000c0a801b722c8d026f2ef01bb6c01fec0706db17950110201b5680000'], 
#'22:22:22:22:22:22': ['45000028f4b5400080060000c0a801b722c8d026f2ef01bb6c01fec1706db17950140000b5680000', '45000034941a400080060000c0a801b736545c9af36201bbb4ef071f000000008002faf055740000020405b40103030801010402', '450000280f78400080060000c0a801b70215b4def1ba01bb0d90699d89dea85150140000796d0000'], 
#'33:33:33:33:33:33': ['4500002827ec400080060000c0a801b75c7b2183f1bc01bb53ec900cd15c27055014000040780000', '45000028941b400080060000c0a801b736545c9af36201bbb4ef0720641864155010faf055680000', '45000028941d400080060000c0a801b736545c9af36201bbb4ef092564186ee35010ff3c55680000']}

#Y hay que contruir el paquete cifrado
#primer paquete de 128:
# 1+ tamaño del paquete mas pequeño de la primera mac+tamaño siguiente paquete+paquete o paquetes +tamaño siguiente clave de cifrado
def montar_paquetes(ampdu):
    print("construyendo el paquete a cifrar")
    paquetes_cifrar = []
    for mac in ampdu:
        ampdu[mac].sort()  # Ordenamos de menor a mayor
        #for paquete in ampdu[mac]:
        #    print(len(paquete))
        
        #paquete128 = [bytes(1+ampdu(mac)[1])]
        if len(ampdu[mac]) >= 2:
            nuevo_paquete = (b'\x80').hex()
            print("longitud primer paquete")
            print(len(ampdu[mac][0]))
            nuevo_paquete += bytes([len(ampdu[mac][0])//2]).hex()
            print("longitud segundo paquete")
            print(len(ampdu[mac][1]))
            nuevo_paquete += bytes([len(ampdu[mac][1])//2]).hex()
            nuevo_paquete += bytes.fromhex(ampdu[mac][0]).hex() + bytes.fromhex(ampdu[mac][1]).hex() 
            print("tamaño nuevo paquete "+str(len(nuevo_paquete)//2))
            bytes_restantes = 128 - len(nuevo_paquete)//2
            print("bytesrestantes 1 "+str(bytes_restantes))
            if bytes_restantes>0:
                nuevo_paquete += bytes.fromhex(ampdu[mac][2]).hex()
            bytes_restantes = 128 - len(nuevo_paquete)//2
            print("bytesrestantes 2 "+str(bytes_restantes))
        # Llenamos con bytes 0 si aún queda espacio
            nuevo_paquete += (b'\x00').hex() * (bytes_restantes)
            if bytes_restantes < 0 :
                nuevo_paquete = nuevo_paquete[:(bytes_restantes*2)]
        
        paquetes_cifrar.append([mac,nuevo_paquete]) 

        

        print("Nuevo paquete de 128 bytes:", nuevo_paquete)
    return paquetes_cifrar      

#print(paquetes_cifrar)


