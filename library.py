"""
BUDA's Library

This file contains a library of functions needed by BUDA to read XML templates, parse .txt files, and return the results
to the user.
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET


class printColors:
    """
    ANSI escape sequences to allow for printing colored text to the terminal.
     - Citation: https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
    """
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    END_FORMATTING = '\033[0m'
    BOLD = '\033[1m'


def joint_parse(template_dir, file_dir):
    """
    Parse a file per a template recursively.
    - This is a handler function that wraps parse_tree() and handles the file I/O associated with the nested function.

    :param template_dir: The directory to the XML template that will be used to parse the file. Must be created in a
                     specific format, as specified in the documentation.
    :param file_dir: The directory to the file that is to be parsed.

    :return: A nested dictionary structure containing the results of parsing the file with the template.
    """

    def convert_flags(string_flags):
        """
        Converts string-forms of regular expression flags into their corresponding integer flag values.

        :param string_flags: A comma separated string of the regular expression flags in text form.

        :return: A bitwise combined form of the regular expression flags in integer form.
        """

        list_string_flags = string_flags.split(",")

        integer_values = {'re.A': 256, 're.ASCII': 256, 're.I': 2, 're.IGNORECASE': 2, 're.L': 4, 're.LOCALE': 4,
                          're.M': 8, 're.MULTILINE': 8, 're.S': 16, 're.DOTALL': 16, 're.X': 64, 're.VERBOSE': 64}

        list_converted_flags = 0

        for flag in list_string_flags:
            try:
                list_converted_flags = list_converted_flags | integer_values[flag]
            except KeyError:
                print(printColors.ERROR + "Error: Regex flag ('" + flag + "') used in XML template is not supported. "
                      "Please check documentation for supported flags." + printColors.END_FORMATTING)
                sys.exit(1)

        return list_converted_flags

    def parse_tree(tree, data):
        """
        Parse a file per an XML tree.

        :param tree: The XML template, stored as an ElementTree, to be used to parse the file.
        :param data: The data, stored as a string, to be parsed.

        :return: A nested dictionary structure containing the results of parsing the file with the template.
        """
        current_dict = {}

        # Read each node in the XML tree at a particular hierarchical level
        # (e.g. multiple sequential, non-nested, containers)
        for node in tree:
            # Handle regular expression flags provided in the XML template
            flags = 0
            if node.get("flags"):
                flags = convert_flags(node.get("flags"))

            # Parse the document with each node, depending on whether it is a container, record, or element
            if node.tag == "container":
                # Identify start and end positions for the container in the document
                try:
                    container_start = re.search(node.get("start"), data, flags=flags).start()
                    container_end = re.search(node.get("end"), data, flags=flags).end()
                except AttributeError:
                    print(printColors.ERROR + "Error: A file ('" + file_dir + "') does not match the XML template  "
                          "provided. Double check the file's structure and the XML template."
                          + printColors.END_FORMATTING)
                    sys.exit(1)

                # Add node to the current_dict object
                if node.get("name") in current_dict:
                    current_dict[node.get("name")].update({node.get("name"): parse_tree(node,
                                                           data[container_start:container_end])})
                else:
                    current_dict[node.get("name")] = parse_tree(node, data[container_start:container_end])
            elif node.tag == "record":
                # Create a list of the starting positions for each instance of the records in the document
                start_records = re.finditer(node.get("start"), data, flags=flags)
                start_records_list = list(start_records)
                num_records = len(start_records_list)

                if not start_records_list:
                    print(printColors.ERROR + "Error: No records of type " + printColors.BOLD + node.get("name") +
                          printColors.END_FORMATTING + printColors.ERROR + " were found in '" + file_dir +
                          printColors.END_FORMATTING + printColors.ERROR + "'. Double check the file's structure and"
                          "the XML template." + printColors.END_FORMATTING)
                    sys.exit(1)

                # Process each instance of the record in the document
                for i in range(num_records):
                    if node.get("group"):
                        record_name = start_records_list[i].group(int(node.get("group")))
                    else:
                        record_name = start_records_list[i].group()

                    # Add instance of record to the current_dict object
                    if node.get("name") in current_dict:
                        if i + 1 < num_records:
                            current_dict[node.get("name")].update(
                                {record_name: parse_tree(node, data[start_records_list[i].start():
                                                         start_records_list[i + 1].end()])})
                        else:
                            current_dict[node.get("name")].update(
                                {record_name: parse_tree(node, data[start_records_list[i].start():len(data)])})
                    else:
                        if i + 1 < num_records:
                            current_dict[node.get("name")] = {record_name: parse_tree(node,
                                                              data[start_records_list[i].start():
                                                              start_records_list[i + 1].end()])}
                        else:
                            current_dict[node.get("name")] = {record_name: parse_tree(node,
                                                              data[start_records_list[i].start():len(data)])}
            else:
                match = re.search(node.text, data, flags=flags)

                try:
                    if node.get("group"):
                        element_value = match.group(int(node.get("group")))
                    else:
                        element_value = match.group()
                except AttributeError:
                    print(printColors.ERROR + "Error: No element of type " + printColors.BOLD + node.get("name") +
                          printColors.END_FORMATTING + printColors.ERROR + " was found in '" + file_dir +
                          printColors.END_FORMATTING + printColors.ERROR + "'. Double check the file's structure and"
                          "the XML template." + printColors.END_FORMATTING)
                    sys.exit(1)

                # Add element to the current_dict object
                if current_dict:
                    current_dict.update({node.get("name"): element_value})
                else:
                    current_dict = {node.get("name"): element_value}

        return current_dict

    # Load the XML template
    xml_tree = ET.parse(template_dir)
    root = xml_tree.getroot()
    nodes = root.findall("*")

    # Load the data file
    try:
        file_object = open(file_dir, "r")
    except IOError:
        print(printColors.ERROR + "Error: Unable to load '" + file_dir + "' into memory. Ensure read access is"
              "available." + printColors.END_FORMATTING)
        sys.exit(1)
    file_data = file_object.read()

    # Parse the data with the XML template
    result = parse_tree(nodes, file_data)
    file_object.close()

    return result


def merge_dict(d1, d2):
    """
    Merge two dictionaries recursively, such that they can have the same keys.
    - Citation: https://stackoverflow.com/questions/10703858/python-merge-multi-level-dictionaries

    :param d1: The first dictionary to be merged.
    :param d2: The second dictionary to be merged.

    :return: A merged dictionary.
    """
    for k, v2 in d2.items():
        v1 = d1.get(k)
        if (isinstance(v1, dict) and
                isinstance(v2, dict)):
            merge_dict(v1, v2)
        else:
            d1[k] = v2


def parse_directory(template_dir, in_dir, out_dir, mode):
    """
    Parse a directory of .txt files with a template (and specific mode) and export the results.
    - This is a file I/O handler function for parse_individual() and parse_aggregate().

    :param template_dir: The directory to the XML template that will be used to parse the file. Must be created in a
                         specific format, as specified in the documentation.
    :param in_dir: The directory to the files to be parsed.
    :param out_dir: The directory where the results of parsing the files will be exported.
    :param mode: The mode to parse the files in, aggregate (True) or individual (False). Aggregate returns a single
                 exported JSON file, aggregate.json, with all of the merged data and no duplicate keys. Individual
                 parses each file separately and returns a .json file named accordingly for each file.
    """

    # Locate all the .txt files in the input directory
    # Citation: https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
    files = []
    try:
        for file in os.listdir(in_dir):
            if file.endswith(".txt"):
                files.append(os.path.join(in_dir, file))
    except FileNotFoundError:
        print(printColors.ERROR + "Error: Could not open '" + in_dir + "' for input. Ensure read access is available."
              + printColors.END_FORMATTING)
        sys.exit(1)

    # Pass the files array to the appropriate function depending on the parsing mode
    if mode:
        parse_aggregate(files, template_dir, out_dir)
    else:
        parse_individual(files, template_dir, in_dir, out_dir)

    print(printColors.SUCCESS + str(len(files)) + " files successfully parsed to '" + out_dir + "'."
          + printColors.END_FORMATTING)


def parse_individual(files, template_dir, in_dir, out_dir):
    """
    Parse a directory of .txt files individually and export the results.

    :param files: An array of directory locations to .txt files to be parsed.
    :param template_dir: The directory to the XML template that will be used to parse the file. Must be created in a
                         specific format, as specified in the documentation.
    :param in_dir: The directory to the files to be parsed.
    :param out_dir: The directory where the results of parsing the files will be exported.
    """

    # Parse the documents and export the results to the output directory
    for file_dir in files:
        result = joint_parse(template_dir, file_dir)
        file_name = out_dir + "/" + file_dir[(len(in_dir) + 1):(len(file_dir) - 4)] + ".json"
        try:
            output = open(file_name, "w")
        except IOError:
            print(printColors.ERROR + "Error: Unable to open '" + file_name + "' for writing. Ensure write access is "
                  "available." + printColors.END_FORMATTING)
            sys.exit(1)
        output.write(json.dumps(result))
        output.close()


def parse_aggregate(files, template_dir, out_dir):
    """
    Parse a directory of .txt files in aggregate and export the results.

    :param files: An array of directory locations to .txt files to be parsed.
    :param template_dir: The directory to the XML template that will be used to parse the file. Must be created in a
                         specific format, as specified in the documentation.
    :param out_dir: The directory where the results of parsing the files will be exported.
    """

    # Populate a merged dictionary with the results of parsing the documents
    result = {}
    for file_dir in files:
        merge_dict(result, joint_parse(template_dir, file_dir))

    # Export the merged dictionary to the output directory
    file_name = out_dir + "/" + "aggregate.json"
    try:
        output = open(file_name, "w")
    except IOError:
        print(printColors.ERROR + "Error: Unable to open '" + file_name + "' for writing. Ensure write access is "
              "available." + printColors.END_FORMATTING)
        sys.exit(1)
    output.write(json.dumps(result))
    output.close()
