import pandas as pd
from flask import jsonify

from BackEnd.Data.data import ForecastData, CompanyData
from BackEnd.Models.arima import Arima, ForecastField
from BackEnd.Models.lstm import convert_df, LSTMModel
from BackEnd.constants import Finance, TechnicalIndicators
from BackEnd.validation import validate_ticker


class TestModels:

    def test_models(self):
        symbol = "NVDA"
        steps = ForecastField(days=21)
        ticker = validate_ticker(symbol=symbol)
        arima_time_series = CompanyData(ticker=ticker).time_series
        lstm_time_series = arima_time_series.copy()

        # # Arima modeling
        instance_arima = Arima(date_column=Finance.date, value_column=Finance.close)
        instance_arima.fit(df=arima_time_series)
        arima_forecast = instance_arima.predict(steps=steps)
        arima_forecast[Finance.date] = arima_forecast[Finance.date].dt.strftime('%m-%d-%Y')

        # LSTM modeling
        instance_lstm = ForecastData(ticker=ticker)
        lstm_df = instance_lstm.lstm(time_series=lstm_time_series)
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

        data = convert_df(
            df=lstm_df,
            time_idx="Count",
            target=Finance.close,
            grouped_dim=["ID"],
            # max_encoder_length=None,
            steps=steps,
            known_cat_vars=["ID"],
            unknown_cont_vars=features,
        )

        lstm_model = LSTMModel.from_dataset(data, n_layers=2, hidden_size=10)
        data_loader = data.to_dataloader()
        x, y = next(iter(data_loader))
        lstm_forecast = lstm_model.forward(dataset=x)

        if len(arima_time_series) > 7:
            arima_time_series = arima_time_series.iloc[0: 7]

        arima_time_series[Finance.date] = arima_time_series[Finance.date].dt.strftime('%m-%d-%Y')
        limit = arima_time_series.iloc[0][Finance.date]

        data_json = {
            Finance.lstm_vals: [round(value[0], 2) for value in lstm_forecast.tolist()[0]] + arima_time_series[Finance.close].to_list(),
            Finance.close: arima_forecast[Finance.close].to_list() + arima_time_series[Finance.close].to_list(),
            Finance.date: arima_forecast[Finance.date].to_list()[::-1] + arima_time_series[Finance.date].to_list(),
            Finance.symbol: ticker,
            Finance.limit: limit
        }

        print(data_json)