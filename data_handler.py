import pandas as pd
import os
import pathlib
from datetime import datetime
from models import *

def get_data_frame(path:str, until:datetime=None):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'],format=r"%d-%m-%y")
    df = df.fillna(-1)
    if until!=None:
        df = df[df['Date']<=until]
    return df

def get_all_data(until:datetime=None):
    dataframes = {}
    for file in pathlib.Path('data/').iterdir():
        file = str(file)
        crop_name = file.split('_price_')[1]
        crop_name = crop_name.split('-upto')[0]
        crop_name = crop_name.split('_upto')[0]
        df = get_data_frame(file,until)
        dataframes[crop_name] = df.to_dict()
    return dataframes

def get_crop_data(crop:str,until:datetime=None):
    dataframes = {}
    for file in pathlib.Path('data/').iterdir():
        file = str(file)
        crop_name = file.split('_price_')[1]
        crop_name = crop_name.split('-upto')[0]
        crop_name = crop_name.split('_upto')[0]
        dataframes[crop_name] = file
    
    if crop in dataframes:
        return get_data_frame(dataframes[crop],until)
    
    return None

def extract_centre_names():
    df = pd.read_csv(pathlib.Path('data/').iterdir()[0])
    return df['Centre_Names'].unique()

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
    if filters['crop'] not in crops:
        return {"message":"Error: crop not found","debug":crops}
    df = get_crop_data()

def get_data(until:datetime,filters:Filter):
    if not filters:
        return get_all_data(until)
    df = get_all_data(until)

    if 'crop' in filters:
        df = get_crop_data(filters['crop'],until)
    if 'from_date' in filters:
        df = df[df['Date']>=filters['from_date']]
    if 'to_date' in filters:
        df = df[df['Date']<=filters['from_date']]
    if 'centre' in filters:
        df = df[df['Centre_Name']==filters['centre']]
    
    return df.to_dict()

        