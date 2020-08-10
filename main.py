from datetime import datetime

from helpers.dateTools import dateTools
from workers.Counter import Counter
from workers.Ssh import Ssh
from workers.XmlReader import XmlReader

comptIte = 0
comptVide = 0
comptIgn = 0
comptIgnList = 0
comptError = 0
comptOk = 0

configReader = XmlReader("config")
addresseSubnet = configReader.readConfigAdresses()
controllerAntenna = configReader.readConfigController()
ignoredIpReader = XmlReader("ignoredIp")
ignoredIp = ignoredIpReader.readIgnoredIp()

compt = 2 ** (32 - addresseSubnet.mask) - 2

print(
    'Addresses: ' + str(addresseSubnet.ip1) + '.' + str(addresseSubnet.ip2) + '.' + str(addresseSubnet.ip3) + '.' + str(
        addresseSubnet.ip4) + ' /' + str(addresseSubnet.mask))
print('User: ' + controllerAntenna.user)
print('Password: ' + controllerAntenna.mdp)
print('Url: http://unifi.' + controllerAntenna.url + ':' + str(controllerAntenna.port) + '/inform')

counter = Counter(addresseSubnet)
sshConnector = Ssh(controllerAntenna)

dateStart = datetime.now()
dtS_string = dateStart.strftime("%d/%m/%Y %H:%M:%S")
print('Start at ' + dtS_string)
while compt > 0:

    ip = counter.counter()
    print(ip, end=': ', flush=True)
    try:
        index = ignoredIp.index(ip)
        del ignoredIp[index]
        comptIgn = comptIgn + 1
        comptIgnList = comptIgnList + 1
        print("Ignored from the list")
    except ValueError:
        result = sshConnector.addtocontroller(ip)
        if result.__eq__('Ok'):
            comptOk = comptOk + 1
        elif result.__eq__('Empty'):
            comptVide = comptVide + 1
        elif result.__eq__('Ignored'):
            comptIgn = comptIgn + 1
        else:
            comptError = comptError + 1

        print(result)

    compt = compt - 1
    comptIte = comptIte + 1

dateEnd = datetime.now()
dtE_string = dateEnd.strftime("%d/%m/%Y %H:%M:%S")
print("Finish at " + dtE_string + " with " + str(comptIte) + " addresses tested: " + str(comptVide) + " empty, " + str(
    comptIgn) + " ignored (" + str(comptIgnList) + " from the list), " + str(
    comptError) + " with error and " + str(comptOk) + " ok")
hours, minutes, seconds = dateTools.convert_timedelta(abs(dateStart - dateEnd))
print("Time: " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds")
