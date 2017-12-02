# Library of Helper Functions for BUDA

import xml.etree.ElementTree as ET
import re


def joint_parse(xml_name, data_name):
    def parse_tree(tree, file):
        current_dict = {}
        for node in tree:
            if node.tag == "container":
                match_start = re.search(node.get("start"), file).start()
                match_end = re.search(node.get("end"), file).end()

                if node.get("name") in current_dict:
                    current_dict[node.get("name")].update({node.get("name"): parse_tree(node, file[match_start:match_end])})
                else:
                    current_dict[node.get("name")] = {node.get("name"): parse_tree(node, file[match_start:match_end])}
            elif node.tag == "record":
                records = re.finditer(node.get("start"), file)
                records_list = list(records)
                length = len(records_list)
                for i in range(length):
                    if node.get("group"):
                        name = records_list[i].group(int(node.get("group")))
                    else:
                        name = records_list[i].group()

                    if node.get("name") in current_dict:
                        if i + 1 < length:
                            current_dict[node.get("name")].update(
                                {name: parse_tree(node, file[records_list[i].start():records_list[i + 1].end()])})
                        else:
                            current_dict[node.get("name")].update(
                                {name: parse_tree(node, file[records_list[i].start():len(file)])})
                    else:
                        if i + 1 < length:
                            current_dict[node.get("name")] = {name: parse_tree(node, file[records_list[i].start():records_list[i + 1].end()])}
                        else:
                            current_dict[node.get("name")] = {name: parse_tree(node, file[records_list[i].start():len(file)])}
            else:
                if node.get("dotall"):
                    match = re.search(node.text, file, flags=16)
                else:
                    match = re.search(node.text, file)

                if node.get("group"):
                    value = match.group(int(node.get("group")))
                else:
                    value = match.group()

                if current_dict:
                    current_dict.update({node.get("name"): value})
                else:
                    current_dict = {node.get("name"): value}
        return current_dict

    # Load the XML file
    xml_tree = ET.parse(xml_name)
    root = xml_tree.getroot()
    nodes = root.findall("*")

    # Load the data file
    file_object = open(data_name, "r")
    data = file_object.read()

    # Initiate joint parsing
    result = parse_tree(nodes, data)
    file_object.close()
    return result
