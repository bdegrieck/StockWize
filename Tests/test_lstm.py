from BackEnd.Data.data import ForecastData, CompanyData
from BackEnd.Models.arima import ForecastField
from BackEnd.Models.lstm import convert_df, LSTMModel
from BackEnd.constants import TechnicalIndicators, Finance


class TestLSTM:

    def test_lstm_model(self):
        ticker="AAPL"
        time_series = CompanyData(ticker=ticker).time_series

        # LSTM modeling
        instance_lstm = ForecastData(ticker=ticker)
        lstm_df = instance_lstm.lstm(time_series=time_series)
        features = [
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
            steps=ForecastField(days=7),
            known_cat_vars=["ID"],
            unknown_cont_vars=features,
        )

        lstm_model = LSTMModel.from_dataset(data, n_layers=2, hidden_size=10)
        lstm_forecast = lstm_model.forward(x=data)
        lstm_vals = [value[0] for value in lstm_forecast.prediction.tolist()[0]]
        print(lstm_vals)