# INF601 - Advanced Programming in Python
# Matt Hogan
# Mini Project 2

import matplotlib.pyplot as plt
import pandas as pd
import os
from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
from adjustText import adjust_text

def make_dir(dir):
    """ Create a new folder if one doesn't exist """
    if not os.path.exists(dir):
        os.mkdir(dir)

def get_kaggle_data(dataset, file_name):
    """
    Gets a file from a Kaggle dataset and returns a relative path to the unzipped csv file
    Must first set API key
    """
    data_dir = "data"
    make_dir(data_dir)
    try:
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_file(dataset, file_name, data_dir)
    except Exception as exc:
        raise Exception("Unable to retrieve Kaggle data") from exc
    
    with ZipFile(os.path.join(data_dir, f"{file_name}.zip")) as zip_object:
        zip_object.extractall(data_dir)
    
    return os.path.join(data_dir, file_name)

def get_cleaned_kaggle_df():
    """ Removes empty values from a csv file and returns a pandas dataframe """
    # Doesn't get Kaggle data if the file already exists
    data = "data\\vending_machine_sales.csv"
    if not os.path.exists(data):
        data = get_kaggle_data("awesomeasingh/vending-machine-sales", "vending_machine_sales.csv")

    df = pd.read_csv(data)
    # Remove rows of data missing a product name
    df = df.dropna(subset=["Product"])
    return df
