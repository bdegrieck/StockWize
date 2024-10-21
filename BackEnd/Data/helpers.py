from typing import Any, Optional

import numpy as np
import pandas as pd
import requests

from BackEnd.constants import AllowedOrientations
from BackEnd.error import EndpointError


def get_raw_data(endpoint: str) -> dict[str, Any]:
    """
    Grabs raw data from api source

    Args:
        endpoint (str): endpoint for api call

    Returns:
        data (dict): dictionary of the data response content
    """
    try:
        response = requests.get(endpoint)
        data = response.json()
    except:
        raise EndpointError(endpoint=endpoint)
    return data


def format_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts column values to floats

    Args:
        df (pd.DataFrame): dataframe of the raw data
    Returns:
        df (pd.DataFrame): dataframe of the corrected value types
    """
    columns = df.columns.tolist()
    for column in columns:
        try:
            df[column] = df[column].astype("float")
        except:
            continue
    df = handle_none(df=df)
    return df


def handle_none(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles "None" values from alpha vantage converted na values

    Args:
        df (pd.DataFrame): dataframe with "None" values in it

    Returns:
        df (pd.DataFrame): dataframe with na values in it
    """
    df = df.replace(to_replace="None", value=np.nan)
    return df


def get_data_df(endpoint: str, key: Optional[str] = None, orient: Optional[AllowedOrientations] = None) -> pd.DataFrame:
    """
    Fetches raw data from a given endpoint, extracts the desired dictionary key, and formats it into a DataFrame.

    Args:
        endpoint (str): The API endpoint to query.
        key (str): The key in the response dictionary to extract the relevant data.
        orient (str): Setting keys of dict to column or index in AllowedOrient
    Returns:
        df (pd.DataFrame): The formatted DataFrame.
    """
    raw_data = get_raw_data(endpoint=endpoint)
    try:
        if key and key in raw_data:
            raw_data = raw_data.get(key)
        if orient:
            df = pd.DataFrame.from_dict(data=raw_data, orient=orient.value)
        else:
            df = pd.DataFrame(data=raw_data)
    except ValueError as e:
            df = pd.DataFrame(raw_data, index=[0])
            print(e)
    return df


def get_raw_api_csv_df(endpoint: str) -> pd.DataFrame:
    """
    To get data from csv data type
    Args:
        endpoint (str): Api endpoint

    Returns:
        df (pd.DataFrame): dataframe of the data
    """
    with requests.Session() as s:
        download = s.get(endpoint)
        decoded_content = download.content.decode('utf-8')
        df = pd.read_csv(pd.compat.StringIO(decoded_content))
    return df
