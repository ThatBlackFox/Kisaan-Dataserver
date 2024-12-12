import pandas as pd
import os
import pathlib
from datetime import datetime, timedelta
from models import *
import holidays
from sklearn.preprocessing import LabelEncoder
import numpy as np
import json

def get_data_frame(path:str, until:datetime=None):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'],format=r"%d-%m-%y")
    # df = df.fillna(-1)
    if until!=None:
        df = df[df['Date']<=until]
    return df

def get_crop_path_pairs(filters:Filter=None):
    crops = {}
    for file in pathlib.Path('data/').iterdir():
        file = str(file)
        crop_name = file.split('_price_')[1]
        crop_name = crop_name.split('-upto')[0]
        crop_name = crop_name.split('_upto')[0]
        if crop_name == "Something":
            continue
        crops[crop_name] = file
    if 'crop' in filters:
        return {filters.crop:crops[filters.crop]}
    return crops

def get_all_data(until:datetime=None,filters:Filter=None):
    dataframes = []
    pairs = get_crop_path_pairs(filters)
    for crop in pairs:
        df = get_data_frame(pairs[crop],until)
        dataframes.append(df)
    df = pd.concat(dataframes, ignore_index=True)
    return df

def get_crop_data(crop:str,until:datetime=None):
    dataframes = get_crop_path_pairs()
    if crop in dataframes:
        return get_data_frame(dataframes[crop],until)
    
    return None

def extract_centre_names():
    df = pd.read_csv(list(pathlib.Path('data/').iterdir())[0])
    return df['Centre_Name'].unique()

def extract_crop_names():
    crops = []
    for file in pathlib.Path('data/').iterdir():
        file = str(file)
        crop_name = file.split('_price_')[1]
        crop_name = crop_name.split('-upto')[0]
        crop_name = crop_name.split('_upto')[0]
        crops.append(crop_name)
    return crops

def filter_crop(crop:str,filters:Filter):
    crops = extract_crop_names()
    if filters.crop not in crops:
        return {"message":"Error: crop not found","debug":crops}
    df = get_crop_data()

def preprocess(df:pd.DataFrame):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = [i.month for i in df['Date']]
    df['Day'] = np.array(i.weekday() for i in df['Date'])
    df['Year'] = [i.year for i in df['Date']]
    india_holidays = holidays.India(years=range(1997, 2016))
    df['Holiday'] = [True if i in india_holidays else False for i in df['Date']]
    df.drop('Date', axis=1, inplace=True)
    le = LabelEncoder()
    df['Centre_Name'] = le.fit_transform(df['Centre_Name'])
    for col in df.columns:
        if col!='Price' and col!='Commodity_Name':
            df[col]=df[col].astype(int)

    for i in range(1, 8):  # Create 7 new columns for the previous 7 days
        df[f'Price_t-{i}'] = df['Price'].shift(i)  
    df.dropna(inplace=True)
    try:
        df.drop('Commodity_Name',axis=1,inplace=True)
    except:
        pass

def apply_filter(df:pd.DataFrame,filters:Filter):
    if filters.crop != None:
        df = df[df['Commodity_Name']==filters.crop]
    if filters.from_date != None:
        filters.from_date-=timedelta(360*10)
        df = df[df['Date']>=filters.from_date]

    if filters.to_date != None:
        filters.to_date-=timedelta(360*10)
        df = df[df['Date']<=filters.to_date]
    if filters.centre != None:
        df = df[df['Centre_Name']==filters.centre]
    return df

def get_data(until:datetime,filters:Filter=None):
    if filters == None:
        return get_all_data(until)
    df = get_all_data(until,filters)
    df = apply_filter(df,filters)
    with open('dump.json','w') as f:
        json.dump(json.loads(df.to_json()), f)
    df.dropna(inplace=True)
    df['Date']+= pd.Timedelta(days=3650-50) 
    df['Price']*=2
    return df.to_dict()