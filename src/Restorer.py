import os
import xml.etree.ElementTree as ET
import lxml.etree as etree


class Restorer:
    fileC = ''
    fileI = ''

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        self.fileC = script_dir + '/files/config.xml'
        self.fileI = script_dir + '/files/ignoredIp.xml'
        if not os.path.exists(script_dir + '/files'):
            access_right = 0o775
            os.mkdir(script_dir + '/files', access_right)

    def restoreFile(self):
        rootC = ET.Element('config')

        addresse = ET.SubElement(rootC, 'addresse')
        ip1 = ET.SubElement(addresse, 'ip1')
        ip2 = ET.SubElement(addresse, 'ip2')
        ip3 = ET.SubElement(addresse, 'ip3')
        ip4 = ET.SubElement(addresse, 'ip4')
        ip1.text = '10'
        ip2.text = '0'
        ip3.text = '0'
        ip4.text = '0'
        mask = ET.SubElement(addresse, 'mask')
        mask.text = '24'
        rangeStart = ET.SubElement(addresse, 'rangeStart')
        rangeEnd = ET.SubElement(addresse, 'rangeEnd')
        rangeStart.text = '0.0.0.0'
        rangeEnd.text = '255.255.255.255'

        controller = ET.SubElement(rootC, 'controller')
        user = ET.SubElement(controller, 'user')
        password = ET.SubElement(controller, 'password')
        user.text = 'ubnt'
        password.text = 'ubnt'
        url = ET.SubElement(controller, 'url')
        port = ET.SubElement(controller, 'port')
        url.text = 'telecomservices.ch'
        port.text = '55880'
        timeout = ET.SubElement(controller, 'timeout')
        timeout.text = '3'

        treeC = ET.ElementTree(rootC)
        treeC.write(self.fileC)
        parserC = etree.XMLParser(remove_blank_text=True)
        formatTreeC = etree.parse(self.fileC, parserC)
        formatTreeC.write(self.fileC, pretty_print=True)
        print(self.fileC + ' restored')

        rootI = ET.Element('ignoredIp')

        single = ET.SubElement(rootI, 'single')
        ipS = ET.SubElement(single, 'ip')
        ipS.text = '0.0.0.0'

        range = ET.SubElement(rootI, 'range')
        ipR = ET.SubElement(range, 'ip')
        ipR.text = '0.0.0.0-0.0.0.0'

        treeI = ET.ElementTree(rootI)
        treeI.write(self.fileI)
        parserI = etree.XMLParser(remove_blank_text=True)
        formatTreeI = etree.parse(self.fileI, parserI)
        formatTreeI.write(self.fileI, pretty_print=True)
        print(self.fileI + ' restored')
