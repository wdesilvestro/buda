# Library of Helper Functions for BUDA

import xml.etree.ElementTree as ET


# Recursively parse an XML tree
# Pass in a list of XML containers from your tree (AKA perform .findall() before sending your tree)
def parse_tree(tree):
    current_dict = {}
    count = 0
    for node in tree:
        if node.tag == "container" or node.tag == "record":
            if node.get("name") in current_dict:
                current_dict[node.get("name")].update(parse_tree(node))
            else:
                current_dict[node.get("name")] = parse_tree(node)
        else:
            if node.get("name") in current_dict:
                current_dict[node.get("name")].update("value")
            else:
                current_dict[node.get("name")] = "value"

    return current_dict


# Example of what it should look like
if node.tag == "record"
    if node.tag in current_dict:
        narrowdocument()
        regexmatch(of narrow version)
        current_dict[node.tag].update({"document's member name = regex match", parse_tree(node)})