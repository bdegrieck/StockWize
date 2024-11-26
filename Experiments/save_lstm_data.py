import json
import os

from BackEnd.Data.data import CompanyData, ForecastData
from BackEnd.constants import TechnicalIndicators, Finance
from Experiments.save_arima_data import LSTMMetaData


def save_lstm_predata():
    tickers = ["META", "AMZN", "AAPL", "NFLX", "GOOGL"]
    meta_data_list = []
    days = [1, 3, 5, 7, 14, 30]
    dates = ['2021-03-26', '2023-07-26', '2022-02-23', '2018-08-07', '2013-10-08', '2021-03-25']

    for ticker in tickers:
        time_series = CompanyData(ticker=ticker).time_series
        arima_series = ForecastData(ticker=ticker).lstm(time_series=time_series)
        for day, date in zip(days, dates):
            meta_data_list.append(
                LSTMMetaData(
                    ticker=ticker,
                    date_series=arima_series[Finance.date].to_list(),
                    close_series=arima_series[Finance.close].to_list(),
                    days=day,
                    date=date,
                    sma=arima_series[TechnicalIndicators.sma].to_list(),
                    ema=arima_series[TechnicalIndicators.ema].to_list(),
                    rsi=arima_series[TechnicalIndicators.rsi].to_list(),
                    bbands_upper=arima_series[TechnicalIndicators.bbands_upper].to_list(),
                    bbands_middle=arima_series[TechnicalIndicators.bbands_middle].to_list(),
                    bbands_lower=arima_series[TechnicalIndicators.bbands_lower].to_list(),
                    adx=arima_series[TechnicalIndicators.adx].to_list()
                ).model_dump()
            )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "lstm_base_data.json")

    with open(file_path, "w") as json_file:
        json.dump(meta_data_list, json_file, indent=4)

    print("saved file")