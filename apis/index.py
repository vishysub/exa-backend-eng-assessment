"""
The GET Details api
"""
import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine

load_dotenv()
app = FastAPI()


def db_connect():
    """
    Creates connection to PostgresDB
    Returns : sqlalchemy.connection
    """
    engine = create_engine(f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}')
    # engine = create_engine('postgresql+psycopg2://pos:password@db:5432/fhirb')
    connection = engine.connect()
    return connection


def FormatResponse(status_code, message):
    """
    Params : status_code : int - httpstatus code
             message : str - Message to be displayed to the user
    Return JSONResponse for Exception cases
    """
    return_res = {"message": message}
    response_context = {
        "BadRequest": {
            "httpStatus": 400,
            "errorType": "Bad Request",

        },
        "InternalServerError": {
            "httpStatus": 500,
            "errorType": "Server Error",
        },
    }

    return_res.update(response_context.get(status_code))
    return JSONResponse(content=return_res, status_code=return_res['httpStatus'])


@app.get("/{resource}")
def details(keys: dict, resource: str, p_stop: bool = False):
    """
    keys -> Search key for the speicified resource
    resource -> path param to specify resource
    """
    result = {}
    requested_fields = keys.get('requested_fields')
    input_data = keys.get('keys')
    if not (isinstance(requested_fields, dict) and isinstance(input_data, dict)):
        return FormatResponse("BadRequest", "Missing/Improper fields")
    try:
        with db_connect() as con:
            fields = "patientid,resource"
            if 'patientid' in input_data.keys():
                query = f"select {fields} from {resource} where patientid in {tuple(i[0] for i in input_data['patientid']) + ('None',)};"
            else:
                condition_fields = json.dumps(input_data)
                where_condition = f"resource @> '{condition_fields}'"
                query = f"select {fields} from {resource} where {where_condition};"
                pid_query = f"select distinct patientid from {resource} where {where_condition};"
                pid = con.execute(pid_query).fetchall()
            data = con.execute(query).fetchall()
        if requested_fields.get(resource) is not None:
            for i in data:
                filter_data = dict(filter(lambda item: item[0] in requested_fields.get(resource), i[1].items()))
                if result.get(i[0], {}).get(resource) is not None:
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
        result['Count'] = len(result.keys())
        return result
    except Exception as e:
        return FormatResponse("InternalServerError", str(e)[:100])


    