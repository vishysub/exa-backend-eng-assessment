"""
The GET Details api
"""
from fastapi import FastAPI
from sqlalchemy import create_engine
import json

engine = create_engine('postgresql+psycopg2://postgres:password@127.0.0.1:5432/fhir')
con = engine.connect()

app = FastAPI()
@app.get("/{resource}")
def details(keys: dict, resource: str, p_stop: bool = False):
    result = {}
    requested_fields = keys.get('requested_fields')

    input_data = keys.get('keys')
    if 'patientid' in input_data.keys():
        query = f"select patientid,resource from {resource} where patientid in {tuple(i[0] for i in input_data['patientid'])};"
    else:
        condition_fields = json.dumps(input_data)
        query = f"select patientid,resource from {resource} where resource @> '{condition_fields}';"
        pid_query = f"select distinct patientid from {resource} where resource @> '{condition_fields}';"
        pid = con.execute(pid_query).fetchall()
    resp = con.execute(query).fetchall()
    data = resp
    filtered_data = []


    if requested_fields.get(resource) is not None:
        for i in data:
            filtered_data.append(dict(filter(lambda item: item[0] in requested_fields.get(resource), i[1].items())))
        result[resource] = filtered_data
        requested_fields.pop(resource)

        if p_stop == False:
            for k,v in requested_fields.items():
                result.update(details({'keys': {'patientid':pid},'requested_fields': {k: v}},k,True))

    else:
        result[resource] = data
    return result
