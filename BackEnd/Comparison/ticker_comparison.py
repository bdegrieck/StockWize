import pandas as pd
from pydantic.v1 import BaseModel

from BackEnd.Data.data import CompanyData
from BackEnd.constants import Finance

class MetaDataComp(BaseModel):
    """
    symbol (str): ticker of the company
    market_cap (float): market cap of the company
    reported_eps (float): latest earnings per share value
    total_revenue (float): latest total revenue of the company
    profit (float): latest total profit of the company
    ppe (float): price per earnings which is price of the stock / eps
    times_series (pd.DataFrame): data frame of time series
    """
    symbol: str
    market_cap: float
    reported_eps: float
    total_revenue: float
    profit: float
    ppe: float
    time_series: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True


class TickerComparison:

    def __init__(self, ticker1: str, ticker2: str):
        self.ticker1 = ticker1
        self.ticker2 = ticker2
        self._ticker1_data = None
        self._ticker2_data = None

    def _set_company_data(self):
        """
        Sets the two ticker data into a MetaDataComp obj and saves to constructor
        """
        ticker_1_instance = CompanyData(ticker=self.ticker1)
        ticker_2_instance = CompanyData(ticker=self.ticker2)

        self._ticker1_data = MetaDataComp(
            symbol=self.ticker1,
            market_cap=ticker_1_instance.overview[Finance.market_cap][0],
            reported_eps=ticker_1_instance.earnings[Finance.reported_eps][0],
            total_revenue=ticker_1_instance.income_statement[Finance.total_revenue][0],
            profit=ticker_1_instance.income_statement[Finance.profit][0],
            ppe=ticker_1_instance.time_series[Finance.close][0] / ticker_1_instance.earnings[Finance.reported_eps][0],
            time_series=ticker_1_instance.time_series
        )

        self._ticker2_data = MetaDataComp(
            symbol=self.ticker2,
            market_cap=ticker_2_instance.overview[Finance.market_cap][0],
            reported_eps=ticker_2_instance.earnings[Finance.reported_eps][0],
            total_revenue=ticker_2_instance.income_statement[Finance.total_revenue][0],
            profit=ticker_2_instance.income_statement[Finance.profit][0],
            ppe=ticker_2_instance.time_series[Finance.close][0] / ticker_2_instance.earnings[Finance.reported_eps][0],
            time_series=ticker_2_instance.time_series
        )

    @property
    def get_ticker1_metadata(self) -> MetaDataComp:
        """
        Returns:
            self._ticker1_data(MetaDataComp): Meta data comp of ticker 1
        """
        if self._ticker1_data is None:
            self._set_company_data()
        return self._ticker1_data

    @property
    def get_ticker2_metadata(self) -> MetaDataComp:
        """
        Returns:
            self._ticker2_data(MetaDataComp): Meta data comp of ticker 2
        """
        if self._ticker2_data is None:
            self._set_company_data()
        return self._ticker2_data

    @property
    def get_difference(self) -> dict[str, float]:
        """
        Calculates the difference of two ticker information against each other

        Returns:
            difference (dict[str, float[): dictionary of the company differences
        """
        if self._ticker1_data is None or self._ticker2_data is None:
            self._set_company_data()

        difference = {
            Finance.market_cap: abs(self._ticker1_data.market_cap - self._ticker2_data.market_cap),
            Finance.reported_eps: abs(self._ticker1_data.reported_eps - self._ticker2_data.reported_eps),
            Finance.total_revenue: abs(self._ticker1_data.total_revenue - self._ticker2_data.total_revenue),
            Finance.profit: abs(self._ticker1_data.profit - self._ticker2_data.profit),
            Finance.PPE: abs(self._ticker1_data.ppe - self._ticker2_data.ppe)
        }
        return difference
