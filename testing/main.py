# Testing out some functions that will be refactored later

import xml.etree.ElementTree as ET
import library as lib
import json

# Parse the template file
tree = ET.parse('template.xml')
root = tree.getroot()
nodes = root.findall("*")

listA = lib.parse_tree(nodes)

jsonConvert = json.dumps(listA)

print(jsonConvert)