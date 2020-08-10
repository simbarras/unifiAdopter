import xml.etree.ElementTree as ET
tree = ET.parse('../files/ignoredIp.xml')
tRoot = tree.getroot()
ignoredIp = []
for child in tRoot:
    ignoredIp.append(child.text)

print(ignoredIp)