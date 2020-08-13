import xml.etree.ElementTree as ET

from beans.Addresse import Addresse
from beans.Controller import Controller


class XmlReader:
    tree = None
    file = ''
    tRoot = None
    ignoredIp = []

    def __init__(self, file):
        self.file = file
        self.tree = ET.parse('./files/' + self.file + '.xml')
        self.tRoot = self.tree.getroot()

    def readIgnoredIp(self):
        for child in self.tRoot:
            self.ignoredIp.append(child.text)
        return self.ignoredIp

    def readConfigAdresses(self):
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
