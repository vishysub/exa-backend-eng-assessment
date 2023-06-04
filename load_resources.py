
import os
import json
import requests
path_to_json_files = 'data/'
URL = "http://localhost:8080/fhir"
json_file_names = [filename for filename in os.listdir(path_to_json_files) if filename.endswith('.json')]
headers = {"Content-Type": "application/fhir+json;charset=utf-8"}
resources = dict()
keys = set()
for json_file_name in json_file_names:
    with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
        json_text = json_file.read()
        r = requests.post(url=URL, data=json_text, headers=headers)
        break;
