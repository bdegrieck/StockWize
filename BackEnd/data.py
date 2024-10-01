import pandas as pd

from BackEnd.endpoints import CompanyEndpoints
from BackEnd.constants import Finance, AlphaVantage, AllowedDataFrameOperations
from BackEnd.helpers import get_data_df, get_raw_data
from BackEnd.news import News


class CompanyData:

    def __init__(self, endpoints: CompanyEndpoints):
        self.endpoints = endpoints


    @property
    def time_series(self) -> pd.DataFrame:
        """
        Returns:
            DataFrame with the following values: Open, High, Low, Close, Volume, Dividend, Split
        """
        endpoint = self.endpoints.time_series
        key = AlphaVantage.time_series_dict
        columns = [
            Finance.open,
            Finance.high,
            Finance.low,
            Finance.non_adjust_close,
            Finance.close,
            Finance.volume,
            Finance.dividend,
            Finance.split
        ]

        renamed_columns = {
            "1. open": Finance.open,
            "2. high": Finance.high,
            "3. low": Finance.low,
            "4. close": Finance.non_adjust_close,
            "5. adjusted close": Finance.close,
            "6. volume": Finance.volume,
            "7. dividend amount": Finance.dividend,
            "8. split coefficient": Finance.split
        }

        filters = {
            AllowedDataFrameOperations.transpose: True,
            AllowedDataFrameOperations.columns: columns,
            AllowedDataFrameOperations.rename: renamed_columns
        }
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def overview(self) -> pd.DataFrame:
        """
        Returns:
            Symbol, Company name, Description of Company, Year high of the stock, Year low of the stock
        """
        endpoint = self.endpoints.overview
        columns = [Finance.symbol, Finance.name, Finance.description, Finance.year_high, Finance.year_low]
        filters = {AllowedDataFrameOperations.columns: columns}
        df = get_data_df(endpoint=endpoint, filters=filters)
        return df

    @property
    def income_statement(self) -> pd.DataFrame:
        """
        Returns:
            Quarter dates, Total revenue quarterly, profit quarterly
        """
        endpoint = self.endpoints.income_statement
        columns = [Finance.fiscal_dates, Finance.total_revenue, Finance.profit]
        filters = {AllowedDataFrameOperations.columns: columns}
        key = AlphaVantage.quarterly_reports_dict
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def cash_flow(self):
        """
        Returns:
            Quarter dates, operating cashflow quarterly, financing cash flow quarterly, from investment cash flow quarterly
        """
        endpoint = self.endpoints.cash_flow
        key = AlphaVantage.quarterly_reports_dict
        columns = [Finance.fiscal_dates, Finance.operating_cash_flow, Finance.from_financing_cash_flow, Finance.from_investment_cash_flow]
        filters = {AllowedDataFrameOperations.columns: columns}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def earnings(self):
        """
        Returns:
            Quarter dates, report dates quarterly, eps quarterly, estimated eps quarterly, surprise percentage quarterly
        """
        endpoint = self.endpoints.earnings
        key = AlphaVantage.quarterly_reports_dict
        columns = [Finance.fiscal_dates, Finance.report_dates, Finance.reported_eps, Finance.estimated_eps, Finance.surprise_percentage]
        filters = {AllowedDataFrameOperations.columns: columns}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def news(self):
        ticker = self.endpoints.ticker
        endpoint = self.endpoints.news
        news_instance = News(ticker=ticker, endpoint=endpoint)
        return news_instance.get_news
