# GetMed - WebApp


## Overview
  * GetMed is an api capable of providing the medical record data (FHIR Format).
  * The api has been built using Python FastApi implementation on PostgresDB deployed using docker.
  * load_resources.py script is provided to load the sample data into the PostgreDB.
  

## Requirements

* `python` Python 3+
* `pip` 
* `Docker`

## Running the webapp  (Setup Postgres DB and Initialize WebApp)
* docker-compose up --build 
## Load the sample data
* Command:python3 utils/load_resources.py

* Once loaded the data would not be deleted even if the app is brought down.
* Without this data you may see errors


#Usage :
 * Url format :[GET] :"http://{hostname}}:{port}}/{resource}"
 * GetMed provides api endpoint customized for the needs of the user.The users can choose the type of data that they requires along with the supporting data required.

##Request and Response Details
 * Ex: To get the claims of a patient given the patient's name.(Resource Defined as per FHIR Standards)
 * To get the patient data the api url {resource} = patient. ("https://.../patient)
   1. keys -> Key value pair to be used as a search element . (Provide patient's name field here)
   2. requested_fields -> Fields that are requried from each resource for all patients who's immunization Status is "completed". 
   #RESPONSE
   1. Count -> Count of Patients in the Response

 
# Sample Request :
{
"keys" : {"id": "b5cb6364-0087-2091-638b-9b23cd827257"},
"requested_fields" : { "immunization":["id"],
                        "patient" :["name"],
                        "claim":["id"]
                      }
}
# Sample Response 
{
    "Count": 1
    "1": {
        "immunization": [
            {
                "id": "b5cb6364-0087-2091-638b-9b23cd827257"
            }
        ],
        "patient": [
            {
                "name": [
                    {
                        "use": "official",
                        "given": [
                            "Everett935"
                        ],
                        "family": "Littel644",
                        "prefix": [
                            "Mr."
                        ]
                    }
                ]
            }
        ],
        "claim": [
            {
                "id": "17ab2629-6969-0b46-f7a1-d8c5346baff2"
            },
            {
                "id": "994c7dcc-b960-af5b-cb55-464d6892e53b"
            },
            {"..."},
            {
                "id": "0d8b13a8-5576-c890-9a04-c15c2097457e"
            },
            {
                "id": "c1243ecf-0017-7c32-6e22-83d2bb47d029"
            }
        ]
    }
}


You can access PostgreSQL on localhost:5432 and Apis on localhost:8000
