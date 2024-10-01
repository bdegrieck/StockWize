from BackEnd.data import CompanyData
from BackEnd.endpoints import CompanyEndpoints


class TestNews:

    def test_news(self):
        ticker = "AAPL"
        endpoints = CompanyEndpoints(ticker=ticker)
        instance = CompanyData(endpoints=endpoints)
        news = instance.news