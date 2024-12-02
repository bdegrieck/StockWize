import os
import json

import pandas as pd
from pydantic import BaseModel
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

from BackEnd.Models.arima import Arima, ForecastField
from BackEnd.constants import Finance

class MetaDataKeys:
    ticker = "ticker"
    date_series = "date_series"
    close_series = "close_series"
    days = "days"
    date = "date"


class MetaDataOutput(BaseModel):
    ticker: str
    mae: float
    date_started: str
    days_forecasted: int

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "arima_base_data.json")

    with open(file_path, "r") as file:
        arima_data = json.load(file)

    output_list = []
    for data in arima_data:
        print(f"Ticker: {data.get(MetaDataKeys.ticker)}")
        print(f"Date Forecast: Starting: {data.get(MetaDataKeys.date)}")
        print(f"Forecasting ahead : {data.get(MetaDataKeys.days)}")
        time_series = pd.DataFrame({
            Finance.date: data.get(MetaDataKeys.date_series),
            Finance.close: data.get(MetaDataKeys.close_series)
        })
        filtered_time_series = time_series[time_series[Finance.date] <= data.get(MetaDataKeys.date)]
        arima_model = Arima(value_column=Finance.close, date_column=Finance.date)
        days = ForecastField(days=data.get(MetaDataKeys.days))
        arima_model.fit(df=filtered_time_series)
        y_pred = arima_model.predict(steps=days)[Finance.close].values
        time_series[Finance.date] = pd.to_datetime(time_series[Finance.date])
        day = pd.Timestamp(data.get(MetaDataKeys.date))
        idx_day = time_series.index[time_series[Finance.date] == day]
        y_true = time_series.iloc[idx_day.item(): idx_day.item() + days.days][Finance.close].tolist()
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
