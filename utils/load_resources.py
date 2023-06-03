'''
Load data to postgres tables;
'''
import os
import json
from sqlalchemy import create_engine
path_to_json_files = 'data/'
from psycopg2.extras import Json
os.chdir('..')
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/fhir')
con = engine.connect()
json_file_names = [filename for filename in os.listdir(path_to_json_files) if filename.endswith('.json')]
unique_id = 1
ser_no = 1
for json_file_name in json_file_names:
    with open(os.path.join(path_to_json_files, json_file_name)) as json_file:
        data = json.load(json_file)

        for res_data in data['entry']:
            resource_type = res_data['resource'].pop('resourceType')
            create_table = f"""CREATE TABLE IF NOT EXISTS {resource_type} ( \
                            id SERIAL PRIMARY KEY, \
                            patientid varchar,
                            resource jsonb
                        );"""
            con.execute(create_table)
            dt = Json(res_data['resource'])
            print(dt)
            query = f"INSERT INTO {resource_type} VALUES ({ser_no},{unique_id},{dt});"
            try:
                val=con.execute(query)
            except Exception as e:
                print("Unsupported Data--------- Skipping")
                pass
            ser_no +=1
    print(f"end of file{json_file_name}")
    unique_id +=1

