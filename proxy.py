from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from models import *
from data_handler import *
from unqlite import UnQLite as unq
from datetime import datetime

db = {}
db['date'] = datetime.today()
app = FastAPI()

@app.get("/centre_names")
async def get_centre_names():
    return {"message":"Attached centres are available","data":list(extract_centre_names())}

@app.get("/crop_names")
async def get_crop_names():
    frames = extract_crop_names()
    return {"message":"Attached crops are available", "data":list(frames.keys())}

@app.get("/crop_prices")
async def get_all_crops(filters:Filter=None):
    frames = get_all_data(until=db['date'],filters=filters)
    return {"message":"Historic data", "data":frames}

@app.get('/')
async def docs():
    return RedirectResponse(app.docs_url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/set_date")
async def set_date(date: DateModel):
    received_date = date.date
    db['date'] = received_date
    return {"message": "Date received successfully", "date": received_date, "debug":str(type((db['date'])))}

@app.get('/get_date')
async def get_date():
    return {"message":"Date is currently set to the same as the field of date", "date":db['date']}



