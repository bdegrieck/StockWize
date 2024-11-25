import os
from time import sleep

from pydantic import BaseModel
import json

from BackEnd.Data.data import CompanyData
from BackEnd.constants import Finance

# TODO grab list of tickers from FAANG
# TODO grab time series info
# TODO grab arima forecasts
# TODO set values for random dates/ intervals you want to forecast ex (erase [10/7/2004 - 10/12/2004] make it a list]) cont.
# TODO do for forecast days [1, 3, 5, 7, 14, 30] at random dates
# TODO do MAE for error metric


class TimeSeriesData(BaseModel):
    ticker: str
    date_series: list
    close_series: list
    days: int
    date: str

    class Config:
        arbitrary_types_allowed=True


tickers = ["META", "AMZN", "AAPL", "NFLX", "GOOGL"]
meta_data_list = []
days = [1, 3, 5, 7, 14, 30]
dates = ['2021-03-26', '2023-07-26', '2022-02-23', '2018-08-07', '2013-10-08', '2021-03-25']

for ticker in tickers:
    time_series = CompanyData(ticker=ticker).time_series
    for day, date in zip(days, dates):
        meta_data_list.append(
            TimeSeriesData(
                ticker=ticker,
                date_series=time_series[Finance.date].to_list(),
                close_series=time_series[Finance.close].to_list(),
                days=day,
                date=date
            ).model_dump()
        )

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "arima_base_data.json")

with open(file_path, "w") as json_file:
    json.dump(meta_data_list, json_file, indent=4)

print("saved file")
