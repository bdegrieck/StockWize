import json
import os

import numpy as np
import pandas as pd
from flask import request
from pydantic.v1 import BaseModel
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from BackEnd.Data.base import TechIndicators
from BackEnd.Models.arima import ForecastField, Arima
from BackEnd.Models.lstm import convert_df, LSTMModel
from BackEnd.constants import Finance, TechnicalIndicators
from Experiments.arima import MetaDataKeys


class MetaDataKeys:
    ticker = "ticker"
    date_series = "date_series"
    close_series = "close_series"
    days = "days"
    date = "date"
    sma = "sma"
    ema = "ema"
    rsi = "rsi"
    bbands_upper = "bbands_upper"
    bbands_middle = "bbands_middle"
    bbands_lower = "bbands_lower"
    adx = "adx"


class MetaDataOutput(BaseModel):
    ticker: str
    mae: float
    date_started: str
    days_forecasted: int

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "lstm_base_data.json")

    with open(file_path, "r") as file:
        arima_data = json.load(file)

    output_list = []
    for data in arima_data:
        print(f"Ticker: {data.get(MetaDataKeys.ticker)}")
        print(f"Date Forecast: Starting: {data.get(MetaDataKeys.date)}")
        print(f"Forecasting ahead : {data.get(MetaDataKeys.days)}")
        steps = ForecastField(days=data.get(MetaDataKeys.days))
        lstm_df = pd.DataFrame({
            Finance.date: data.get(MetaDataKeys.date_series),
            Finance.close: data.get(MetaDataKeys.close_series),
            TechnicalIndicators.sma: data.get(MetaDataKeys.sma),
            TechnicalIndicators.ema: data.get(MetaDataKeys.ema),
            TechnicalIndicators.rsi: data.get(MetaDataKeys.rsi),
            TechnicalIndicators.bbands_lower: data.get(MetaDataKeys.bbands_lower),
            TechnicalIndicators.bbands_middle: data.get(MetaDataKeys.bbands_middle),
            TechnicalIndicators.bbands_upper: data.get(MetaDataKeys.bbands_upper),
            TechnicalIndicators.adx: data.get(MetaDataKeys.adx)
        })
        lstm_df = lstm_df.reset_index(drop=False, names="Count")
        lstm_df["ID"] = "1"

        features = [
            Finance.close,
            TechnicalIndicators.bbands_upper,
            TechnicalIndicators.bbands_middle,
            TechnicalIndicators.bbands_lower,
            TechnicalIndicators.ema,
            TechnicalIndicators.rsi,
            TechnicalIndicators.sma,
            TechnicalIndicators.adx
        ]

        df_converted = convert_df(
            df=lstm_df,
            time_idx="Count",
            target=Finance.close,
            grouped_dim=["ID"],
            # max_encoder_length=None,
            steps=steps,
            known_cat_vars=["ID"],
            unknown_cont_vars=features,
        )

        lstm_model = LSTMModel.from_dataset(df_converted, n_layers=2, hidden_size=10)
        data_loader = df_converted.to_dataloader()
        x, y = next(iter(data_loader))
        lstm_forecast = lstm_model.forward(dataset=x)
        y_pred = [round(value[0], 2) for value in lstm_forecast.tolist()[0]]

        lstm_df[Finance.date] = pd.to_datetime(lstm_df[Finance.date])
        day = pd.Timestamp(data.get(MetaDataKeys.date))
        idx_day = lstm_df.index[lstm_df[Finance.date] == day]
        y_true = lstm_df.iloc[idx_day.item(): idx_day.item() + steps.days][Finance.close].tolist()
        mae = mean_absolute_error(y_true=y_true, y_pred=y_pred)
        mse = mean_squared_error(y_true=y_true, y_pred=y_pred)
        r_squared = r2_score(y_true=y_true, y_pred=y_pred)
        print(f"MAE: {mae}")
        print(f"MSE: {mse}")
        print(f"R Squared: {r_squared}")
        output_list.append(MetaDataOutput(
                ticker=data.get(MetaDataKeys.ticker),
                mae=mae,
                date_started=data.get(MetaDataKeys.date),
                days_forecasted=data.get(MetaDataKeys.days)
            )
        )

    print(output_list)