import xml.etree.ElementTree as ET
import os
import lxml.etree as etree

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
        return Addresse(ip1, ip2, ip3, ip4, mask)

    def readConfigController(self):
        controllerXml = self.tRoot.find('controller')
        user = controllerXml.find('user').text
        mdp = controllerXml.find('mdp').text
        url = controllerXml.find('url').text
        port = controllerXml.find('port').text
        timeout = controllerXml.find('timeout').text
        return Controller(user, mdp, url, port, timeout)

    def writeConfig(self, addresseSubnet, controllerAntenna):
        result = False

        adresseXml = self.tRoot.find('addresse')
        adresseXml.find('ip1').text = str(addresseSubnet.ip1)
        adresseXml.find('ip2').text = str(addresseSubnet.ip2)
        adresseXml.find('ip3').text = str(addresseSubnet.ip3)
        adresseXml.find('ip4').text = str(addresseSubnet.ip4)
        adresseXml.find('mask').text = str(addresseSubnet.mask)

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
