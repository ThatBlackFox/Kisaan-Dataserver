from fastapi import FastAPI
from models import *
from data_handler import *
from unqlite import UnQLite as unq
from datetime import datetime

db = {}
db['date'] = datetime.today()
app = FastAPI()

@app.get("/crop/{crop}")
async def get_crop(crop):
    frames = get_crop_data(crop,until=db['date'])
    if crop in frames:
        return {"message":"Historic data", "data":frames[crop]}
    else:
        frames = get_all_data(until=db['date'])
        return {"message":"Crop not found, only the attached crops are available", "data":list(frames.keys())}

@app.get("/crop_names")
async def get_crop_names():
    frames = get_all_data(until=db['date'])
    return {"message":"Attached crops are available", "data":list(frames.keys())}

@app.get("/all_crops")
async def get_all_crops():
    frames = get_all_data(until=db['date'])
    return {"message":"Historic data", "data":frames}

@app.post("/set_date")
async def set_date(date: DateModel):
    received_date = date.date
    db['date'] = received_date
    return {"message": "Date received successfully", "date": received_date, "debug":str(type((db['date'])))}

@app.get('/get_date')
async def get_date():
    return {"message":"Date is currently set to the same as the field of date", "date":db['date']}



