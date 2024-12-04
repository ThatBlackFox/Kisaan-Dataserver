import pandas as pd
import os
import pathlib
from datetime import datetime
from models import *
import json

def get_data_frame(path:str, until:datetime=None):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'],format=r"%d-%m-%y")
    df = df.fillna(-1)
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

def apply_filter(df:pd.DataFrame,filters:Filter):
    if filters.crop != None:
        df = df[df['Commodity_Name']==filters.crop]
    if filters.from_date != None:
        df = df[df['Date']>=filters.from_date]
    if filters.to_date != None:
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
    return df.to_dict()