from BackEnd.Data.data import CompanyData
from BackEnd.Models.arima import Arima, Forecast
from BackEnd.constants import Finance


class TestArima:

    def test_arima(self):

        # test for apple for 1 day forecast
        value_column = Finance.close
        date_column = Finance.date
        ticker = "AAPL"
        company_instance = CompanyData(ticker=ticker)
        time_series = company_instance.time_series
        arima_instance = Arima(time_series=time_series, value_column=value_column, date_column=date_column)
        arima_instance.fit()
        forecast = arima_instance.predict(steps=Forecast(days=1))
        assert not forecast[Finance.forecast].isna().any()
        assert len(forecast) == 1

        # test 7 day forecast with tesla
        ticker = "TSLA"
        company_instance = CompanyData(ticker=ticker)
        time_series = company_instance.time_series
        arima_instance = Arima(time_series=time_series, value_column=value_column, date_column=date_column)
        arima_instance.fit()
        forecast = arima_instance.predict(steps=Forecast(days=7))
        assert not forecast[Finance.forecast].isna().any()
        assert len(forecast) == 7

        # test 30 day forecast with microsoft
        ticker = "MSFT"
        company_instance = CompanyData(ticker=ticker)
        time_series = company_instance.time_series
        arima_instance = Arima(time_series=time_series, value_column=value_column, date_column=date_column)
        arima_instance.fit()
        forecast = arima_instance.predict(steps=Forecast(days=30))
        assert not forecast[Finance.forecast].isna().any()
        assert len(forecast) == 30