import requests

from BackEnd.api import CompanyEndpoints, MicroEndpoints, CalenderEndpoints, TechIndEndpoints


class TestEndpoints:


    def test_company_endpoints(self):
        ticker = "AAPL"
        instance = CompanyEndpoints(ticker=ticker)
        assert requests.get(instance.time_series).status_code == 200
        assert requests.get(instance.overview).status_code == 200
        assert requests.get(instance.earnings).status_code == 200
        assert requests.get(instance.cash_flow).status_code == 200
        assert requests.get(instance.income_statement).status_code == 200
        assert requests.get(instance.balance_sheet).status_code == 200

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
