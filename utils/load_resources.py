
import os
import json
import requests
from sqlalchemy import create_engine
path_to_json_files = 'data/'
os.chdir('..')
#
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/fhir')
con = engine.connect()
#
# query = """INSERT INTO bundle VALUES (1,  '{"name": {"fire":"test","age": 23}, "tags": ["Improvements", "Office"], "finished": true}');"""
json_file_names = [filename for filename in os.listdir(path_to_json_files) if filename.endswith('.json')]
# headers = {"Content-Type": "application/fhir+json;charset=utf-8"}
# resources = dict()
# keys = set()
for json_file_name in json_file_names:
    with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
        data = json.load(json_file)
        # data = data.replace("true", "\"true\"")
        # data = data.replace("false", "\"false\"")
        print(json.dumps(data))
        # query = """INSERT INTO bundle VALUES (3,'{"name": {"fire":true,"age": 23}, "tags": ["Improvements", "Office"], "finished": true}');"""
        query = f"INSERT INTO bundle VALUES (2,\'{json.dumps(data)}\');"
        print(query)
        x=con.execute(query)
        break;
