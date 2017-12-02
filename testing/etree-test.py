import xml.etree.ElementTree as ET
tree = ET.parse('test.xml')
root = tree.getroot()

children = root.findall("*")

country1 = children[0]

for element in country1.findall("*"):
    print(element)
