from fastapi import FastAPI
from models import *
from unqlite import UnQLite as unq

db = unq('data.db')
app = FastAPI()

@app.get("/wheat")
async def wheat():
    return {"message":"Hello World"}

@app.post("/set_date")
async def set_date(date_model: DateModel):
    received_date = date_model.date
    db['date'] = received_date
    return {"message": "Date received successfully", "date": received_date}

@app.get('/get_date')
async def get_date():
    return {"message":"Date is currently set to the same as the field of date", "date":db['date']}


