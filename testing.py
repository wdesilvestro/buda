# Testing out some functions that will be refactored later

import json


def convert_dicts(list_dicts):
    string_dicts = ""

    for item in list_dicts:
        string_dicts += str(item)[1:13] + ","

    return string_dicts[0:(len(string_dicts) - 1)]


test = [{"test1": "A"}, {"test2": "B"}, {"test3": "C"}]

converted = convert_dicts(test)

print(json.dumps(converted))