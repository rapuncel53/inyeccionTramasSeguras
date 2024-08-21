
def claves(mac, tamaño):
    claveps = None
    clavexs = None
    archivo = mac + ".txt"
    with open(archivo, "r") as file:
            lines = file.readlines()
            if tamaño == -1:
                claveps = int(lines[1].replace("psnew.1: ", "").strip())
                clavexs = int(lines[2].replace("xsnew.1: ", "").strip())
            elif tamaño <= 128:
                claveps = int(lines[5].replace("psnew: ", "").strip())
                clavexs = int(lines[6].replace("xsnew: ", "").strip())
            elif tamaño <= 144:
                claveps = int(lines[9].replace("psnew: ", "").strip())
                clavexs = int(lines[10].replace("xsnew: ", "").strip())
            elif tamaño <= 160:
                claveps = int(lines[13].replace("psnew: ", "").strip())
                clavexs = int(lines[14].replace("xsnew: ", "").strip())
            elif tamaño <= 176:
                claveps = int(lines[17].replace("psnew: ", "").strip())
                clavexs = int(lines[18].replace("xsnew: ", "").strip())
            elif tamaño <= 192:
                claveps = int(lines[21].replace("psnew: ", "").strip())
                clavexs = int(lines[22].replace("xsnew: ", "").strip())
            elif tamaño <= 208:
                claveps = int(lines[25].replace("psnew: ", "").strip())
                clavexs = int(lines[26].replace("xsnew: ", "").strip())
            elif tamaño <= 224:
                claveps = int(lines[29].replace("psnew: ", "").strip())
                clavexs = int(lines[30].replace("xsnew: ", "").strip())
            elif tamaño <= 240:
                claveps = int(lines[33].replace("psnew: ", "").strip())
                clavexs = int(lines[34].replace("xsnew: ", "").strip())
            elif tamaño <= 256:
                claveps = int(lines[37].replace("psnew: ", "").strip())
                clavexs = int(lines[38].replace("xsnew: ", "").strip())
            elif tamaño <= 272:
                claveps = int(lines[41].replace("psnew: ", "").strip())
                clavexs = int(lines[42].replace("xsnew: ", "").strip())
            elif tamaño <= 288:
                claveps = int(lines[45].replace("psnew: ", "").strip())
                clavexs = int(lines[46].replace("xsnew: ", "").strip())
            elif tamaño <= 304:
                claveps = int(lines[49].replace("psnew: ", "").strip())
                clavexs = int(lines[50].replace("xsnew: ", "").strip())
            elif tamaño <= 320:
                claveps = int(lines[53].replace("psnew: ", "").strip())
                clavexs = int(lines[54].replace("xsnew: ", "").strip())
            elif tamaño <= 336:
                claveps = int(lines[57].replace("psnew: ", "").strip())
                clavexs = int(lines[58].replace("xsnew: ", "").strip())
            elif tamaño <= 352:
                claveps = int(lines[61].replace("psnew: ", "").strip())
                clavexs = int(lines[62].replace("xsnew: ", "").strip())
            elif tamaño <= 368:
                claveps = int(lines[65].replace("psnew: ", "").strip())
                clavexs = int(lines[66].replace("xsnew: ", "").strip())
            elif tamaño <= 384:
                claveps = int(lines[69].replace("psnew: ", "").strip())
                clavexs = int(lines[70].replace("xsnew: ", "").strip())
            elif tamaño <= 400:
                claveps = int(lines[73].replace("psnew: ", "").strip())
                clavexs = int(lines[74].replace("xsnew: ", "").strip())
            elif tamaño <= 416:
                claveps = int(lines[77].replace("psnew: ", "").strip())
                clavexs = int(lines[78].replace("xsnew: ", "").strip())
            elif tamaño <= 432:
                claveps = int(lines[81].replace("psnew: ", "").strip())
                clavexs = int(lines[82].replace("xsnew: ", "").strip())
            elif tamaño <= 448:
                claveps = int(lines[85].replace("psnew: ", "").strip())
                clavexs = int(lines[86].replace("xsnew: ", "").strip())
            elif tamaño <= 464:
                claveps = int(lines[89].replace("psnew: ", "").strip())
                clavexs = int(lines[90].replace("xsnew: ", "").strip())
            elif tamaño <= 480:
                claveps = int(lines[93].replace("psnew: ", "").strip())
                clavexs = int(lines[94].replace("xsnew: ", "").strip())
            elif tamaño <= 496:
                claveps = int(lines[97].replace("psnew: ", "").strip())
                clavexs = int(lines[98].replace("xsnew: ", "").strip())
            elif tamaño <= 512:
                claveps = int(lines[101].replace("psnew: ", "").strip())
                clavexs = int(lines[102].replace("xsnew: ", "").strip())
    
    # if mac == "11:11:11:11:11:11":
        
    #         if tamaño <= 128:
    #             claveps = int(lines[1].strip("psnew: "))
    #             clavexs = int(lines[2].strip("xsnew: "))
            
    # if mac == "22:22:22:22:22:22":
    #     with open("resultados.txt", "r") as file:
    #         lines = file.readlines()
    #         if tamaño <= 128:
    #             claveps = int(lines[5].strip())
    #             clavexs = int(lines[6].strip())
            
    # if mac == "33:33:33:33:33:33":
    #     with open("resultados.txt", "r") as file:
    #         lines = file.readlines()    
    #         if tamaño <= 128:
    #             claveps = int(lines[9].strip())
    #             clavexs = int(lines[10].strip())
    
    #print ("claves ",claveps,clavexs)
    return claveps, clavexs

# claveps, clavexs = claves("11:11:11:11:11:11", 123)
# print(claveps, clavexs)