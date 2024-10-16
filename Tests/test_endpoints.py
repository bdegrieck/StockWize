import requests
import pytest
from unittest.mock import patch
from BackEnd.endpoints import CompanyEndpoints, MicroEndpoints, CalenderEndpoints, TechIndEndpoints, get_raw_data

class TestEndpoints:

    def test_company_endpoints(self):
        ticker = "AAPL"
        instance = CompanyEndpoints(ticker=ticker)
        assert requests.get(instance.time_series).status_code == 200
        assert requests.get(instance.overview).status_code == 200
        assert requests.get(instance.earnings).status_code == 200
        assert requests.get(instance.cash_flow).status_code == 200
        assert requests.get(instance.income_statement).status_code == 200
        assert requests.get(instance.news).status_code == 200

    def test_micro_endpoints(self):
        instance = MicroEndpoints()
        assert requests.get(instance.unemployment_rate).status_code == 200
        assert requests.get(instance.real_gdp).status_code == 200
        assert requests.get(instance.cpi).status_code == 200
        assert requests.get(instance.inflation).status_code == 200
        assert requests.get(instance.federal_funds_rate).status_code == 200
        assert requests.get(instance.retail_sales).status_code == 200

    def test_calender_endpoints(self):
        ticker = "AAPL"
        instance = CalenderEndpoints(ticker=ticker)
        assert requests.get(instance.company_earnings).status_code == 200
        assert requests.get(instance.upcoming_earnings).status_code == 200

    def test_technical_indicator_endpoints(self):
        ticker = "AAPL"
        instance = TechIndEndpoints(ticker=ticker)
        assert requests.get(instance.sma).status_code == 200
        assert requests.get(instance.ema).status_code == 200
        assert requests.get(instance.rsi).status_code == 200
        assert requests.get(instance.bbands).status_code == 200
        assert requests.get(instance.adx).status_code == 200

    @patch('BackEnd.api.requests.get')  # Mock requests.get to prevent real API calls
    def test_get_raw_data(self, mock_get):
        # Setup the mock to return a successful response with dummy data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"key": "value"}

        # Define the API URL and parameters for the test
        api_url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": "AAPL",
            "apikey": "test_api_key",
            "outputsize": "full",
            "datatype": "json"
        }

        # Call the get_raw_data function
        data = get_raw_data(api_url, params)

        # Assert that the mock was called as expected and that data matches
        mock_get.assert_called_once_with(api_url, params=params)
        assert data == {"key": "value"}



    def test_get_raw_data_success(self):
        api_url = "https://www.alphavantage.co/query"
        params = {"function": "TIME_SERIES_DAILY_ADJUSTED", "symbol": "AAPL", "apikey": "CRU63X7J4COJ46F2"}

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"Time Series (Daily)": {"2024-01-01": {"1. open": "100.00"}}}

            result = get_raw_data(api_url, params)

            assert result == {"Time Series (Daily)": {"2024-01-01": {"1. open": "100.00"}}}
            mock_get.assert_called_once_with(api_url, params=params)

    def test_get_raw_data_invalid_endpoint(self):
        api_url = "https://www.alphavantage.co/invalid"
        params = {"apikey": "CRU63X7J4COJ46F2"}

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            mock_get.return_value.text = "Not Found"

            with pytest.raises(ValueError, match="Failed to fetch data: 404, Not Found"):
                get_raw_data(api_url, params)

    def test_get_raw_data_api_error(self):
        api_url = "https://www.alphavantage.co/query"
        params = {"function": "TIME_SERIES_DAILY_ADJUSTED", "symbol": "INVALID", "apikey": "CRU63X7J4COJ46F2"}

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"Error Message": "Invalid symbol"}

            with pytest.raises(ValueError, match="API Error: Invalid symbol"):
                get_raw_data(api_url, params)