"""
The GET Details api
"""
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def details():
    return {"Test": "This is a test"}