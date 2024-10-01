from BackEnd.data import MicroData, TechIndData
from BackEnd.endpoints import MicroEndpoints, TechIndEndpoints


class TestMicro:

    def test_micro_data(self):

        ticker = "AAPL"
        endpoints = TechIndEndpoints(ticker=ticker)
        instance = TechIndData(endpoints=endpoints)
        data = instance.adx