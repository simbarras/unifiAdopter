import os
import xml.etree.ElementTree as ET

from beans.Addresse import Addresse
from beans.Controller import Controller


# import lxml.etree as etree


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
        for child in self.tRoot:
            self.ignoredIp.append(child.text)
        return self.ignoredIp

    def readConfigAddresses(self):
        adresseXml = self.tRoot.find('addresse')
        ip1 = adresseXml.find('ip1').text
        ip2 = adresseXml.find('ip2').text
        ip3 = adresseXml.find('ip3').text
        ip4 = adresseXml.find('ip4').text
        mask = adresseXml.find('mask').text
        rangeStart = adresseXml.find('rangeStart').text
        rangeEnd = adresseXml.find('rangeEnd').text
        return Addresse(ip1, ip2, ip3, ip4, mask, rangeStart, rangeEnd)

    def readConfigController(self):
        controllerXml = self.tRoot.find('controller')
        user = controllerXml.find('user').text
        mdp = controllerXml.find('mdp').text
        url = controllerXml.find('url').text
        port = controllerXml.find('port').text
        timeout = controllerXml.find('timeout').text
        return Controller(user, mdp, url, port, timeout)

    def writeConfig(self, addressSubnet, controllerAntenna):
        result = False

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
        controllerXml.find('mdp').text = str(controllerAntenna.mdp)
        controllerXml.find('url').text = str(controllerAntenna.url)
        controllerXml.find('port').text = str(controllerAntenna.port)
        controllerXml.find('timeout').text = str(controllerAntenna.timeout)

        self.writeFile()

        result = True
        return result

    def writeIgnoredIp(self, ignoredIp):
        result = False

        childs = self.tRoot.findall('ip')
        for child in childs:
            self.tRoot.remove(child)

        for ip in ignoredIp:
            ipTree = ET.SubElement(self.tRoot, 'ip')
            ipTree.text = ip

        self.writeFile()

        result = True
        return result

    def writeFile(self):
        self.tree.write(self.file)
        parser = etree.XMLParser(remove_blank_text=True)
        formatTree = etree.parse(self.file, parser)
        formatTree.write(self.file, pretty_print=True)
