'''
Script to check the resource types in each json file

Resource Types Available {'Bundle':{'resourceType', 'entry', 'type'}}
'''

import os
import json

path_to_json_files = 'data/'
json_file_names = [filename for filename in os.listdir(path_to_json_files) if filename.endswith('.json')]
resources = dict()
keys = set()
for json_file_name in json_file_names:
    with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
        json_text = json.load(json_file)
        res_type = json_text.get("resourceType")

        if res_type in resources.keys():
            resources[res_type].update(set(json_text.keys()))
        else:
            resources[res_type] = set(json_text.keys())


print("Resource Types Available", resources)