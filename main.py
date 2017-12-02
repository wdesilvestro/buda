# Testing out some functions that will be refactored later

import library as lib
import json

# Parse the template file
data = lib.joint_parse("template.xml", "minutes.txt")

jsonConvert = json.dumps(data)

print(jsonConvert)