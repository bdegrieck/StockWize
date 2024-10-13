import numpy as np
import pandas as pd
import requests
from typing import Any, Optional

from BackEnd.error import EndpointError
from BackEnd.constants import AllowedDataFrameOperations


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
    Formats the date columns as pd.datetime and converts values to floats

    Args:
        df (pd.DataFrame): dataframe of the raw data
    Returns:
        df (pd.DataFrame): dataframe of the corrected value types
    """
    columns = df.columns.tolist()
    for column in columns:
        try:
            df[column] = df[column].astype("float")
            continue
        except:
            pass
        try:
            df[column] = pd.to_datetime(df[column])
        except:
            pass
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


def get_data_df(endpoint: str, key: Optional[str] = None, filters: Optional[AllowedDataFrameOperations] = None) -> pd.DataFrame:
    """
    Fetches raw data from a given endpoint, extracts the desired dictionary key, and formats it into a DataFrame.

    Args:
        endpoint (str): The API endpoint to query.
        key (str): The key in the response dictionary to extract the relevant data.
        filters (AllowedDataFrameOperations): Allowed datafraem operations
    Returns:
        df (pd.DataFrame): The formatted DataFrame.
    """
    raw_data = get_raw_data(endpoint=endpoint)
    if key is not None:
        raw_data = raw_data.get(key)

    if filters.orient is None:
        filters.orient = "columns"

    try:
        df = pd.DataFrame.from_dict(data=raw_data, orient=filters.orient)
    except ValueError:
        df = pd.DataFrame(raw_data, index=[0])

    if filters is not None:
        if filters.transpose is not None:
            df = df.transpose()
        if filters.drop is not None:
            df = df.drop(columns=filters.get(AllowedDataFrameOperations.drop))
        if filters.rename is not None:
            df = df.rename(columns=filters.get(AllowedDataFrameOperations.rename))
        if filters.columns is not None:
            df = df[filters.get(AllowedDataFrameOperations.columns)]

    df = format_df(df=df)
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
