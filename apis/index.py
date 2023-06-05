"""
The GET Details api
REQUEST :
        {"keys" : {"status": "completed"},
    "requested_fields" : {"patient" :["id","name"],
                        "immunization": ["id","meta"]
    }
    }


RESPONSE :

"""
from fastapi import FastAPI
from sqlalchemy import create_engine
import json
import logging

engine = create_engine('postgresql+psycopg2://postgres:password@db:5432/fhir')
con = engine.connect()
app = FastAPI()

logger = logging.getLogger("logging")

def FormatResponse(status_code, message):
    return_res = {"message": message}
    response_context = {
        "BadRequest": {
            "httpStatus": 400,
            "errorType": "Bad Request",

        },
        "Unauthorized": {"httpStatus": 401, "errorType": "Unauthorized"},
        "Forbidden": {"httpStatus": 403, "errorType": "Forbidden"},
        "NotFound": {
            "httpStatus": 404,
            "errorType": "Not Found",

        },
        "Conflict": {"httpStatus": 409, "errorType": "Conflict"},
        "InternalServerError": {
            "httpStatus": 500,
            "errorType": "Server Error",
        },
    }

    return_res.update(response_context.get(status_code))
    return return_res


@app.get("/{resource}")
def details(keys: dict, resource: str, p_stop: bool = False):
    result = {}
    requested_fields = keys.get('requested_fields')
    input_data = keys.get('keys')
    if not isinstance(requested_fields,dict):
        return FormatResponse("BadRequest", "Missing/Improper request_fields field")

    if 'patientid' in input_data.keys():
        query = f"select patientid,resource from {resource} where patientid in {tuple(i[0] for i in input_data['patientid']) + ('None',)};"
    else:
        condition_fields = json.dumps(input_data)
        query = f"select patientid,resource from {resource} where resource @> '{condition_fields}';"
        pid_query = f"select distinct patientid from {resource} where resource @> '{condition_fields}';"
        pid = con.execute(pid_query).fetchall()
    data = con.execute(query).fetchall()
    filtered_data = []
    if requested_fields.get(resource) is not None:
        for i in data:
            filter_data = dict(filter(lambda item: item[0] in requested_fields.get(resource), i[1].items()))
            if result.get(i[0],{}).get(resource) is not None:
                result[i[0]][resource].append(filter_data)
            else:
                result[i[0]] = {resource: [filter_data]}

        requested_fields.pop(resource)

        if p_stop == False:
            for res, fields in requested_fields.items():
                response = details({'keys': {'patientid': pid}, 'requested_fields': {res: fields}}, res, True)
                for i in pid:
                    result[i[0]].update(response[i[0]])

    else:
        result[resource] = data
    return result
