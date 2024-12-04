import pandas as pd
import os
import pathlib
from datetime import datetime

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
        return {crop:get_data_frame(dataframes[crop],until).to_dict()}
    
    return {}

def get_names():
    crops = []
    for file in pathlib.Path('data/').iterdir():
        file = str(file)
        crop_name = file.split('_price_')[1]
        crop_name = crop_name.split('-upto')[0]
        crop_name = crop_name.split('_upto')[0]
        crops.append(crop_name)
    return crops