import os
import xml.etree.ElementTree as ET

import lxml.etree as etree

from Counter import Counter
from beans.Addresse import Addresse
from beans.Controller import Controller


class XmlReader:
    tree = None
    file = ''
    tRoot = None
    ignoredIp = []

    def __init__(self, file):
        script_dir = os.path.dirname(__file__)
        self.file = script_dir + '/files/' + file + '.xml'
        self.tree = ET.parse(self.file)
        self.tRoot = self.tree.getroot()

    def readIgnoredIp(self):
        if os.path.exists(self.file):
            singleIp = self.tRoot.find('single')
            rangeIp = self.tRoot.find('range')
            for child in singleIp:
                self.ignoredIp.append(child.text)
            for child in rangeIp:
                for ip in self.readRange(child.text):
                    self.ignoredIp.append(ip)
        else:
            self.ignoredIp = []
            print(self.file + ' not found, please restore with unifiA-restore')

        return self.ignoredIp


    def readRange(self, range):
        rips, ripe = range.split('-', 2)
        ips1, ips2, ips3, ips4 = rips.split('.', 4)
        ipe1, ipe2, ipe3, ipe4 = ripe.split('.', 4)
        ips1 = int(ips1)
        ips2 = int(ips2)
        ips3 = int(ips3)
        ips4 = int(ips4)
        ipe1 = int(ipe1)
        ipe2 = int(ipe2)
        ipe3 = int(ipe3)
        ipe4 = int(ipe4)

        ipl1 = (ipe1 - ips1)
        ipl2 = (ipe2 - ips2)
        ipl3 = (ipe3 - ips3)
        ipl4 = (ipe4 - ips4)
        comptAddr = (((ipl1 * 256 + ipl2) * 256 + ipl3) * 256 + ipl4) - 1

        ignoredIp = []
        address = Addresse(ips1, ips2, ips3, ips4, 0, '0.0.0.0', '0.0.0.0')
        counter = Counter(address)
        while comptAddr > 0:
            ip = counter.counter()
            ignoredIp.append(ip)
            comptAddr = comptAddr - 1
        return ignoredIp

    def readConfigAddresses(self):
        if os.path.exists(self.file):
            adresseXml = self.tRoot.find('addresse')
            ip1 = adresseXml.find('ip1').text
            ip2 = adresseXml.find('ip2').text
            ip3 = adresseXml.find('ip3').text
            ip4 = adresseXml.find('ip4').text
            mask = adresseXml.find('mask').text
            rangeStart = adresseXml.find('rangeStart').text
            rangeEnd = adresseXml.find('rangeEnd').text
            result = Addresse(ip1, ip2, ip3, ip4, mask, rangeStart, rangeEnd)
        else:
            result = Addresse(10, 0, 0, 0, 24, '0.0.0.0', '255.255.255.255')
            print(self.file + ' not found, please restore with unifiA-restore')
        return result

    def readConfigController(self):
        if os.path.exists(self.file):
            controllerXml = self.tRoot.find('controller')
            user = controllerXml.find('user').text
            mdp = controllerXml.find('password').text
            url = controllerXml.find('url').text
            port = controllerXml.find('port').text
            timeout = controllerXml.find('timeout').text
            result = Controller(user, mdp, url, port, timeout)
        else:
            result = Controller('ubnt', 'ubnt', 'telecomservices.ch', '55880', '3')
            print(self.file + ' not found, please restore with unifiA-restore')
        return result

    def writeConfig(self, addressSubnet, controllerAntenna):
        result = False
        if os.path.exists(self.file):
            adresseXml = self.tRoot.find('addresse')
            adresseXml.find('ip1').text = str(addressSubnet.ip1)
            adresseXml.find('ip2').text = str(addressSubnet.ip2)
            adresseXml.find('ip3').text = str(addressSubnet.ip3)
            adresseXml.find('ip4').text = str(addressSubnet.ip4)
            adresseXml.find('mask').text = str(addressSubnet.mask)
            adresseXml.find('rangeStart').text = str(addressSubnet.rangeStart1) + '.' + str(
                addressSubnet.rangeStart2) + '.' + str(
                addressSubnet.rangeStart3) + '.' + str(addressSubnet.rangeStart4)
            adresseXml.find('rangeEnd').text = str(addressSubnet.rangeEnd1) + '.' + str(
                addressSubnet.rangeEnd2) + '.' + str(
                addressSubnet.rangeEnd3) + '.' + str(addressSubnet.rangeEnd4)

            controllerXml = self.tRoot.find('controller')
            controllerXml.find('user').text = str(controllerAntenna.user)
            controllerXml.find('password').text = str(controllerAntenna.mdp)
            controllerXml.find('url').text = str(controllerAntenna.url)
            controllerXml.find('port').text = str(controllerAntenna.port)
            controllerXml.find('timeout').text = str(controllerAntenna.timeout)

            self.writeFile()

            result = True
        else:
            print(self.file + ' not found, please restore with unifiA-restore')
        return result

    def writeIgnoredIp(self, ignoredIp):
        result = False
        if os.path.exists(self.file):
            singleIp = self.tRoot.find('single')
            self.tRoot.remove(singleIp)
            rangeIp = self.tRoot.find('range')
            self.tRoot.remove(rangeIp)

            singleIp = ET.SubElement(self.tRoot, 'single')
            rangeIp = ET.SubElement(self.tRoot, 'range')
            rangeIpEx = ET.SubElement(rangeIp, 'ip')
            rangeIpEx.text = '0.0.0.0-0.0.0.0'

            for ip in ignoredIp:
                ipTree = ET.SubElement(singleIp, 'ip')
                ipTree.text = ip

            self.writeFile()

            result = True
        else:
            print(self.file + ' not found, please restore with unifiA-restore')
        return result

    def writeFile(self):
        self.tree.write(self.file)
        parser = etree.XMLParser(remove_blank_text=True)
        formatTree = etree.parse(self.file, parser)
        formatTree.write(self.file, pretty_print=True)
