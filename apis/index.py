"""
The GET Details api
"""
from fastapi import FastAPI

from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/fhir')
con = engine.connect()

app = FastAPI()
@app.get("/")
def details():
    return {"Test": "This is a test"}