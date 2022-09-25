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

def get_product_dataframe(df):
    """
    Takes in a dataframe with vending machine transactions
    Returns a dataframe of best selling vending machine products along with the quanity of the product sold, the gross revenue the product made, and the product's category
    """
    product_data =  [
        [
            product,
            df.loc[df["Product"] == product, "RQty"].sum(),
            df.loc[df["Product"] == product, "RPrice"].sum(),
            df[df["Product"] == product].iloc[0].Category
        ]
        for product in df.Product.unique()
    ]
    product_df = pd.DataFrame(product_data, columns=["product_name", "quantity_sold", "gross_revenue", "category"])

    # Remove prodcuts who do not meet best selling thresholds
    product_df.drop(product_df.index[product_df['quantity_sold'] < 100], inplace=True)
    product_df.drop(product_df.index[product_df['gross_revenue'] < 200], inplace=True)

    def add_missing_categories(df):
        """
        Adds a category to products missing one.
        For this data some Canada Dry drinks are missing the carbonated category, Starbucks drinks are missing non carbonated, and the rest of the missing categories are for food.
        """
        df.loc[df.isnull()] = "Carbonated" if "Canada Dry" in df["product_name"] else "Non Carbonated" if "Starbucks" in df["product_name"] else "Food"
        return df

    product_df = product_df.apply(add_missing_categories, axis=1)
    return product_df
