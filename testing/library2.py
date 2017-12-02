# Library of Helper Functions for BUDA

import xml.etree.ElementTree as ET
import re


def joint_parse(xml_name, data_name):
    def parse_tree(tree, beg_pos, end_pos):
        current_dict = {}
        for node in tree:
            print(node)
            print(str(beg_pos) + " " + str(end_pos))
            if node.tag == "container":
                match_start = re.search(node.get("start"), data[beg_pos:end_pos]).start()
                match_end = re.search(node.get("end"), data[beg_pos:end_pos]).end()

                if node.tag in current_dict:
                    current_dict[node.tag].update({node.get("name"): parse_tree(node, match_start, match_end)})
                else:
                    current_dict[node.tag] = {node.get("name"): parse_tree(node, match_start, match_end)}
            elif node.tag == "record":
                records = re.finditer(node.get("start"), data[beg_pos:end_pos])
                records_list = list(records)
                print(records_list[0].start())
                length = len(records_list)
                for i in range(length):
                    if node.tag in current_dict:
                        if i + 1 < length:
                            current_dict[node.tag].update(
                                {records_list[i].group(): parse_tree(node, records_list[i].start(),
                                                                     records_list[i + 1].end())})
                        else:
                            current_dict[node.tag].update(
                                {records_list[i].group(): parse_tree(node, records_list[i].start(),
                                                                     end_pos)})
                    else:
                        if i + 1 < length:
                            current_dict[node.tag] = {records_list[i].group(): parse_tree(node, records_list[i].start(),
                                                                                          records_list[i + 1].end())}
                        else:
                            current_dict[node.tag] = {records_list[i].group(): parse_tree(node, records_list[i].start(),
                                                                                          end_pos)}
            else:
                match = re.search(node.text, data[beg_pos:end_pos])

                if node.tag in current_dict:
                    current_dict[node.tag].update({node.get("name"): match.group()})
                else:
                    current_dict[node.tag] = {node.get("name"): match.group()}
        return current_dict

    # Load the XML file
    xml_tree = ET.parse(xml_name)
    root = xml_tree.getroot()
    nodes = root.findall("*")

    # Load the data file
    file_object = open(data_name, "r")
    data = file_object.read()

    # Initiate joint parsing
    result = parse_tree(nodes, 0, len(data))
    file_object.close()
    print(result)
    return result
