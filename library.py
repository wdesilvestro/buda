# Library of Helper Functions for BUDA

import xml.etree.ElementTree as ET
import re
import os
import json


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


def parse_individual(template_dir, in_dir, out_dir):
    # Locate all the .txt files in the input directory
    # Citation: https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
    files = []
    for file in os.listdir(in_dir):
        if file.endswith(".txt"):
            files.append(os.path.join(in_dir, file))

    # Convert each file to a .txt in the output directory
    for fdir in files:
        result = joint_parse(template_dir, fdir)
        output = open(out_dir + "/" + fdir[(len(in_dir) + 1):(len(fdir) - 4)] + ".json", "w")
        output.write(json.dumps(result))
        output.close()


# Citation: https://stackoverflow.com/questions/10703858/python-merge-multi-level-dictionaries
def merge_dict(d1, d2):
    for k, v2 in d2.items():
        v1 = d1.get(k)
        if (isinstance(v1, dict) and
                isinstance(v2, dict)):
            merge_dict(v1, v2)
        else:
            d1[k] = v2


def parse_aggregate(template_dir, in_dir, out_dir):
    files = []
    for file in os.listdir(in_dir):
        if file.endswith(".txt"):
            files.append(os.path.join(in_dir, file))

    # Convert each file to a .txt in the output directory
    # pdf2txt.extract_text(files, "/output")
    result = {}
    for fdir in files:
        merge_dict(result, joint_parse(template_dir, fdir))

    output = open(out_dir + "/" + "aggregate.json", "w")
    output.write(json.dumps(result))
    output.close()
