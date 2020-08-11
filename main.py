from datetime import datetime

from helpers.DateTools import DateTools
from helpers.XmlReader import XmlReader
from workers.Counter import Counter
from workers.Ssh import Ssh

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

print(
    'Addresses: ' + str(addresseSubnet.ip1) + '.' + str(addresseSubnet.ip2) + '.' + str(addresseSubnet.ip3) + '.' + str(
        addresseSubnet.ip4) + ' /' + str(addresseSubnet.mask))
print('User: ' + controllerAntenna.user)
print('Password: ' + controllerAntenna.mdp)
print('Url: http://unifi.' + controllerAntenna.url + ':' + str(controllerAntenna.port) + '/inform')
print('Timeout: ' + str(controllerAntenna.timeout) + ' (Number of seconds before an address is set as empty)')

modify = input('Would you like to modify the informations ? (y/n) [n]: ')

if modify.__eq__('y'):
    subnet = input('subnet [' + str(addresseSubnet.ip1) + '.' + str(addresseSubnet.ip2) + '.' + str(
        addresseSubnet.ip3) + '.' + str(addresseSubnet.ip4) + ']: ')
    if subnet:
        ip1, ip2, ip3, ip4 = subnet.split('.', 4)
        addresseSubnet.ip1 = int(ip1)
        addresseSubnet.ip2 = int(ip2)
        addresseSubnet.ip3 = int(ip3)
        addresseSubnet.ip4 = int(ip4)

    mask = input('Mask [' + str(addresseSubnet.mask) + ']: ')
    if mask:
        addresseSubnet.mask = int(mask)

    user = input('User [' + controllerAntenna.user + ']: ')
    if user:
        controllerAntenna.user = user

    password = input('Password [' + controllerAntenna.mdp + ']: ')
    if password:
        controllerAntenna.mdp = password

    url = input('Url [' + controllerAntenna.url + ']: ')
    if url:
        controllerAntenna.url = url

    port = input('Port [' + str(controllerAntenna.port) + ']: ')
    if port:
        controllerAntenna.port = int(port)

    timeout = input('Timeout: [' + str(controllerAntenna.timeout) + ']: ')
    if timeout:
        controllerAntenna.mdp = int(timeout)

    seeAddressesIgnored = input('Would you like to see the ignored ip ? (y/n) [n]: ')

    if seeAddressesIgnored.__eq__('y'):
        addIp = input('Tip the addresse you will add (None = no): ')
        for ip in ignoredIp:
            print(ip)

        while addIp:
            ignoredIp.append(addIp)
            print(addIp)
            addIp = input('')

compt = 2 ** (32 - addresseSubnet.mask) - 2
counter = Counter(addresseSubnet)
sshConnector = Ssh(controllerAntenna)

print('###############################################################################################################')
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

print('###############################################################################################################')

dateEnd = datetime.now()
dtE_string = dateEnd.strftime("%d/%m/%Y %H:%M:%S")
print("Finish at " + dtE_string + " with " + str(comptIte) + " addresses tested: " + str(comptVide) + " empty, " + str(
    comptIgn) + " ignored (" + str(comptIgnList) + " from the list), " + str(
    comptError) + " with error and " + str(comptOk) + " ok")
hours, minutes, seconds = DateTools.convert_timedelta(abs(dateStart - dateEnd))
print("Time: " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds")
