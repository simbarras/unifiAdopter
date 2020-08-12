from datetime import datetime

from helpers.DateTools import DateTools
from helpers.XmlReader import XmlReader
from workers.Counter import Counter
from workers.Ssh import Ssh


class Ctrl:
    compt = 0
    comptIte = 0
    comptVide = 0
    comptIgn = 0
    comptIgnList = 0
    comptError = 0
    comptOk = 0

    addresseSubnet = None
    controllerAntenna = None
    ignoredIp = []

    counter = None
    sshConnector = None

    dateStart = None
    dateEnd = None

    def __init__(self):
        configReader = XmlReader("config")
        self.addresseSubnet = configReader.readConfigAdresses()
        self.controllerAntenna = configReader.readConfigController()
        ignoredIpReader = XmlReader("ignoredIp")
        self.ignoredIp = ignoredIpReader.readIgnoredIp()

    def load(self):
        print(
            'Addresses: ' + str(self.addresseSubnet.ip1) + '.' + str(self.addresseSubnet.ip2) + '.' + str(
                self.addresseSubnet.ip3) + '.' + str(
                self.addresseSubnet.ip4) + ' /' + str(self.addresseSubnet.mask))
        print('User: ' + self.controllerAntenna.user)
        print('Password: ' + self.controllerAntenna.mdp)
        print('Url: http://unifi.' + self.controllerAntenna.url + ':' + str(self.controllerAntenna.port) + '/inform')
        print('Timeout: ' + str(
            self.controllerAntenna.timeout) + ' (Number of seconds before an address is set as empty)')
        print('Ignored ip: ' + str(len(self.ignoredIp)))

    def preStart(self):
        modify = input('Would you like to modify the informations ? (y/n) [n]: ')

        if modify.__eq__('y'):

            continu = input('Would you like to continue ? (y/n) [y]: ')

            if continu.__eq__('n'):
                return False
            else:
                subnet = input(
                    'subnet [' + str(self.addresseSubnet.ip1) + '.' + str(self.addresseSubnet.ip2) + '.' + str(
                        self.addresseSubnet.ip3) + '.' + str(self.addresseSubnet.ip4) + ']: ')
                if subnet:
                    ip1, ip2, ip3, ip4 = subnet.split('.', 4)
                    self.addresseSubnet.ip1 = int(ip1)
                    self.addresseSubnet.ip2 = int(ip2)
                    self.addresseSubnet.ip3 = int(ip3)
                    self.addresseSubnet.ip4 = int(ip4)

                mask = input('Mask [' + str(self.addresseSubnet.mask) + ']: ')
                if mask:
                    self.addresseSubnet.mask = int(mask)

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
                    self.controllerAntenna.mdp = int(timeout)

                seeAddressesIgnored = input('Would you like to see the ignored ip ? (y/n) [n]: ')

                if seeAddressesIgnored.__eq__('y'):
                    print('Tip the addresse you will add (None = no): ')
                    for ip in self.ignoredIp:
                        print(ip)

                    addIp = input('')
                    while addIp:
                        self.ignoredIp.append(addIp)
                        print(addIp)
                        addIp = input('')

        return True

    def start(self):
        self.compt = 2 ** (32 - self.addresseSubnet.mask) - 2
        self.counter = Counter(self.addresseSubnet)
        self.sshConnector = Ssh(self.controllerAntenna)

        print(
            '###############################################################################################################')
        self.dateStart = datetime.now()
        dtS_string = self.dateStart.strftime("%d/%m/%Y %H:%M:%S")
        print('Start at ' + dtS_string)

    def scan(self):
        while self.compt > 0:

            ip = self.counter.counter()
            print(ip, end=': ', flush=True)
            try:
                index = self.ignoredIp.index(ip)
                del self.ignoredIp[index]
                self.comptIgn = self.comptIgn + 1
                self.comptIgnList = self.comptIgnList + 1
                print("Ignored from the list")
            except ValueError:
                result = self.sshConnector.addtocontroller(ip)
                if result.__eq__('Ok'):
                    self.comptOk = self.comptOk + 1
                elif result.__eq__('Empty'):
                    self.comptVide = self.comptVide + 1
                elif result.__eq__('Ignored'):
                    self.comptIgn = self.comptIgn + 1
                else:
                    self.comptError = self.comptError + 1

                print(result)

            self.compt = self.compt - 1
            self.comptIte = self.comptIte + 1

    def finish(self):
        print(
            '###############################################################################################################')

        self.dateEnd = datetime.now()
        dtE_string = self.dateEnd.strftime("%d/%m/%Y %H:%M:%S")
        print("Finish at " + dtE_string + " with " + str(self.comptIte) + " addresses tested: " + str(
            self.comptVide) + " empty, " + str(
            self.comptIgn) + " ignored (" + str(self.comptIgnList) + " from the list), " + str(
            self.comptError) + " with error and " + str(self.comptOk) + " ok")
        hours, minutes, seconds = DateTools.convert_timedelta(abs(self.dateStart - self.dateEnd))
        print("Time: " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds")
