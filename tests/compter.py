
ip1 = 192
ip2 = 168
ip3 = 1
ip4 = 0
mask = 22
user = 'ubnt'
password = 'ubnt'
comptIte = 0
comptVide = 0
comptIgn = 0
comptOk = 0

compt = 2**(32-mask) - 2

while compt > 0:
    if ip4==255:
        ip4 = 0
        if ip3==255:
            ip3 = 0
            if ip2 == 255:
                ip2 = 0
                if ip1 == 255:
                    ip1 = 0
                else:
                    ip1 = ip1 + 1
            else:
                ip2 = ip2 + 1
        else:
            ip3 = ip3 + 1
    else:
        ip4 = ip4+1

    host = str(ip1) + "." + str(ip2) + "." + str(ip3) + "." + str(ip4)
    print(host)

    compt = compt-1
    comptIte = comptIte+1

print("finish with "+str(comptIte)+" adresses tested: "+str(comptVide)+" empty, "+str(comptIgn)+" ignored and "+str(comptOk)+" ok")
