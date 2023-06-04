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
        query = f"select patientid,resource from {resource} where patientid = '{input_data['patientid']}';"
    else:
        condition_fields = json.dumps(input_data)
        query = f"select patientid,resource from {resource} where resource @> '{condition_fields}';"
    pid = 1
    resp = con.execute(query).fetchall()

    data = resp[0][1]


    if requested_fields.get(resource) is not None:
        result[resource] = dict(filter(lambda item: item[0] in requested_fields.get(resource), data.items()))

        requested_fields.pop(resource)

        if p_stop == False:
            for k,v in requested_fields.items():
                result.update(details({'keys':{'patientid':pid},'requested_fields': {k: v}},k,True))

    else:
        result[resource] = data
    return result
