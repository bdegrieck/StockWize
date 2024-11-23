import pandas as pd
from flask import jsonify

from BackEnd.Data.data import ForecastData, CompanyData
from BackEnd.Models.arima import Arima, ForecastField
from BackEnd.Models.lstm import convert_df, LSTMModel
from BackEnd.constants import Finance, TechnicalIndicators
from BackEnd.validation import validate_ticker


class TestModels:

    def test_models(self):
        symbol = "AAPL"
        steps = ForecastField(days=7)
        ticker = validate_ticker(symbol=symbol)
        time_series = CompanyData(ticker=ticker).time_series
        lstm_copy = time_series.copy()

        # # Arima modeling
        instance_arima = Arima(date_column=Finance.date, value_column=Finance.close)
        instance_arima.fit(df=time_series)
        forecast = instance_arima.predict(steps=steps)

        # LSTM modeling
        instance_lstm = ForecastData(ticker=ticker)
        lstm_df = instance_lstm.lstm(time_series=lstm_copy)
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

        if len(time_series) > 7:
            time_series = time_series.iloc[0: 7]

        df = pd.concat(
            [time_series[[Finance.date, Finance.close]],
             forecast[[Finance.date, Finance.close]]]
        )

        df.sort_values(by=Finance.date, inplace=True, ascending=False)
        df[Finance.date] = df[Finance.date].dt.strftime('%m-%d-%Y')
        limit = time_series.iloc[0][Finance.date].strftime('%m-%d-%Y')

        data_json = {
            Finance.lstm_vals: [value[0] for value in lstm_forecast.prediction.tolist()[0]],
            Finance.close: df[Finance.close].to_list(),
            Finance.date: df[Finance.date].to_list(),
            Finance.symbol: ticker,
            Finance.limit: limit
        }

        jsonify(data_json)