from datetime import datetime

from XmlReader import XmlReader
from DateTools import DateTools
from Counter import Counter
from Ssh import Ssh


class Ctrl:
    compt = 0
    comptIte = 0
    comptVide = 0
    comptIgn = 0
    comptIgnList = 0
    comptError = 0
    comptOk = 0

    addAutomaticallyIp = False

    configReader = None
    ignoredIpReader = None
    addressSubnet = None
    controllerAntenna = None
    ignoredIp = []

    counter = None
    sshConnector = None

    dateStart = None
    dateEnd = None

    def __init__(self):
        self.configReader = XmlReader("config")
        self.addressSubnet = self.configReader.readConfigAddresses()
        self.controllerAntenna = self.configReader.readConfigController()
        self.ignoredIpReader = XmlReader("ignoredIp")
        self.ignoredIp = self.ignoredIpReader.readIgnoredIp()

    def load(self):
        print(
            'Addresses: ' + str(self.addressSubnet.ip1) + '.' + str(self.addressSubnet.ip2) + '.' + str(
                self.addressSubnet.ip3) + '.' + str(
                self.addressSubnet.ip4) + ' /' + str(self.addressSubnet.mask))
        print('User: ' + self.controllerAntenna.user)
        print('Password: ' + self.controllerAntenna.mdp)
        print('Url: http://unifi.' + self.controllerAntenna.url + ':' + str(self.controllerAntenna.port) + '/inform')
        print('Timeout: ' + str(
            self.controllerAntenna.timeout) + ' (Number of seconds before an address is set as empty)')
        print('Ignored ip: ' + str(len(self.ignoredIp)))

    def prestart(self):
        modify = input('Would you like to modify the informations ? (y/n) [n]: ')

        if modify.__eq__('y'):

            subnet = input(
                'subnet [' + str(self.addressSubnet.ip1) + '.' + str(self.addressSubnet.ip2) + '.' + str(
                    self.addressSubnet.ip3) + '.' + str(self.addressSubnet.ip4) + ']: ')
            if subnet:
                ip1, ip2, ip3, ip4 = subnet.split('.', 4)
                self.addressSubnet.ip1 = int(ip1)
                self.addressSubnet.ip2 = int(ip2)
                self.addressSubnet.ip3 = int(ip3)
                self.addressSubnet.ip4 = int(ip4)

            mask = input('Mask [' + str(self.addressSubnet.mask) + ']: ')
            if mask:
                self.addressSubnet.mask = int(mask)

            user = input('User [' + self.controllerAntenna.user + ']: ')
            if user:
                self.controllerAntenna.user = user

            password = input('Password [' + self.controllerAntenna.mdp + ']: ')
            if password:
                self.controllerAntenna.mdp = password

            url = input('Url [' + self.controllerAntenna.url + ']: ')
            if url:
                self.controllerAntenna.url = url

            port = input('Port [' + str(self.controllerAntenna.port) + ']: ')
            if port:
                self.controllerAntenna.port = int(port)

            timeout = input('Timeout: [' + str(self.controllerAntenna.timeout) + ']: ')
            if timeout:
                self.controllerAntenna.timeout = int(timeout)

            overwriteConfigFile = input('Would you like to overwrite config file ? (y/n) [n]: ')
            if overwriteConfigFile.__eq__('y'):
                if not self.configReader.writeConfig(self.addressSubnet, self.controllerAntenna):
                    print('Error when writing the configuration file')

        seeAddressesIgnored = input('Would you like to see the ignored ip ? (y/n) [n]: ')

        if seeAddressesIgnored.__eq__('y'):
            print('Tip the address you will add (None = no): ')
            for ip in self.ignoredIp:
                print(ip)

            modifAddressesIgnored = input('Would you like to modify the ignored ip list? (y/n) [n]: ')
            if modifAddressesIgnored.__eq__('y'):
                print('Writes the replacement address (None = no change / - = delete): ')
                newIgnoredIp = []
                for ip in self.ignoredIp:
                    newAddress = input(ip+' :')
                    if not newAddress:
                        newIgnoredIp.append(ip)
                    elif not newAddress.__eq__('-'):
                        newIgnoredIp.append(newAddress)

                print('Writes new address (None = no): ')
                addIp = input('')
                while addIp:
                    newIgnoredIp.append(addIp)
                    addIp = input('')

                self.ignoredIp = newIgnoredIp

                overwriteIpfile = input('Would you like to add new ip to the file ? (y/n) [n]: ')
                if overwriteIpfile.__eq__('y'):
                    if not self.ignoredIpReader.writeIgnoredIp(self.ignoredIp):
                        print('Error when writing the IP file')

        runScan = input('Would you like to run the scan ? (y/n) [y]: ')
        if runScan.__eq__('n'):
            return False

        addressesIgnored = input('Would you like to add automatically the non-valid ip to the file ? (y/n) [n]: ')
        if addressesIgnored.__eq__('y'):
            self.addAutomaticallyIp = True

        return True

    def start(self):
        self.compt = 2 ** (32 - self.addressSubnet.mask) - 2
        self.counter = Counter(self.addressSubnet)
        self.sshConnector = Ssh(self.controllerAntenna)

        print(
            '#########################################################################################################')
        self.dateStart = datetime.now()
        dtS_string = self.dateStart.strftime("%d/%m/%Y %H:%M:%S")
        print('Start at ' + dtS_string)

    def scan(self):
        while self.compt > 0:

            ip = self.counter.counter()
            print(ip, end=': ', flush=True)
            try:
                self.ignoredIp.index(ip)
                self.comptIgn = self.comptIgn + 1
                self.comptIgnList = self.comptIgnList + 1
                print("Ignored from the list")
            except ValueError:
                result = self.sshConnector.addtocontroller(ip)
                if result.__eq__('Ok'):
                    self.comptOk = self.comptOk + 1
                elif result.__eq__('Empty'):
                    if self.addAutomaticallyIp:
                        self.ignoredIp.append(ip)
                    self.comptVide = self.comptVide + 1
                elif result.__eq__('Ignored'):
                    if self.addAutomaticallyIp:
                        self.ignoredIp.append(ip)
                    self.comptIgn = self.comptIgn + 1
                else:
                    if self.addAutomaticallyIp:
                        self.ignoredIp.append(ip)
                    self.comptError = self.comptError + 1

                print(result)

            self.compt = self.compt - 1
            self.comptIte = self.comptIte + 1

    def finish(self):
        print(
            '#########################################################################################################')
        if self.addAutomaticallyIp:
            self.ignoredIpReader.writeIgnoredIp(self.ignoredIp)
        self.dateEnd = datetime.now()
        dtE_string = self.dateEnd.strftime("%d/%m/%Y %H:%M:%S")
        print("Finish at " + dtE_string + " with " + str(self.comptIte) + " addresses tested: " + str(
            self.comptVide) + " empty, " + str(
            self.comptIgn) + " ignored (" + str(self.comptIgnList) + " from the list), " + str(
            self.comptError) + " with error and " + str(self.comptOk) + " ok")
        hours, minutes, seconds = DateTools.convert_timedelta(abs(self.dateStart - self.dateEnd))
        print("Time: " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds")
