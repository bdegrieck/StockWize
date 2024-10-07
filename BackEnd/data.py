import pandas as pd

from BackEnd.endpoints import CompanyEndpoints, MicroEndpoints, TechIndEndpoints, CalenderEndpoints
from BackEnd.constants import Finance, AlphaVantage, AllowedDataFrameOperations
from BackEnd.helpers import get_data_df, get_raw_api_csv_df
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
    def cash_flow(self) -> pd.DataFrame:
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
    def earnings(self) -> pd.DataFrame:
        """
        Returns:
            Quarter dates, report dates quarterly, eps quarterly, estimated eps quarterly, surprise percentage quarterly
        """
        endpoint = self.endpoints.earnings
        key = AlphaVantage.quarterly_earnings_dict
        columns = [Finance.fiscal_dates, Finance.report_dates, Finance.reported_eps, Finance.estimated_eps, Finance.surprise_percentage]
        filters = {AllowedDataFrameOperations.columns: columns}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def news(self) -> str:
        ticker = self.endpoints.ticker
        endpoint = self.endpoints.news
        news_instance = News(ticker=ticker, endpoint=endpoint)
        return news_instance.get_news

class MicroData:

    def __init__(self):
        self.endpoints = MicroEndpoints()


    @property
    def real_gdp(self) -> pd.DataFrame:
        """
        Returns:
            Real GDP quarterly at the beginning of the year, Date quarterly
        """
        endpoint = self.endpoints.real_gdp
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df

    @property
    def cpi(self) -> pd.DataFrame:
        """
        Returns:
            cpi value, first day of the monthy dates
        """
        endpoint = self.endpoints.cpi
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df

    @property
    def inflation(self) -> pd.DataFrame:
        """
        Returns:
            inflation percentage per year, dates first day of the year
        """
        endpoint = self.endpoints.inflation
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df

    @property
    def federal_funds_rate(self) -> pd.DataFrame:
        """
        Returns:
            federal funds rate monthly, first day of the month for dates
        """
        endpoint = self.endpoints.federal_funds_rate
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df

    @property
    def retail_sales (self) -> pd.DataFrame:
        """
        Returns:
            returns the retail sales in millions per month, date is first day of every month
        """
        endpoint = self.endpoints.retail_sales
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df

    @property
    def unemployment_rate(self) -> pd.DataFrame:
        """
        Returns:
`           Unemployment rate at the beginning of the month
        """
        endpoint = self.endpoints.unemployment_rate
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df


class TechIndData:

    def __init__(self, endpoints: TechIndEndpoints):
        self.endpoints = endpoints

    @property
    def sma(self) -> pd.DataFrame:
        """
        Returns:
`           SMA value, weekly date
        """
        endpoint = self.endpoints.sma
        key = AlphaVantage.sma
        filters = {AllowedDataFrameOperations.transpose: True}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def ema(self) -> pd.DataFrame:
        """
        Returns:
`           EMA values, weekly date
        """
        endpoint = self.endpoints.ema
        key = AlphaVantage.ema
        filters = {AllowedDataFrameOperations.transpose: True}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def rsi(self) -> pd.DataFrame:
        """
        Returns:
`           RSI values, weekly date
        """
        endpoint = self.endpoints.rsi
        key = AlphaVantage.rsi
        filters = {AllowedDataFrameOperations.transpose: True}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def bbands(self) -> pd.DataFrame:
        """
        Returns:
`           Bbands values, weekly date
        """
        endpoint = self.endpoints.bbands
        key = AlphaVantage.bbands
        filters = {AllowedDataFrameOperations.transpose: True}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def adx(self) -> pd.DataFrame:
        """
        Returns:
`           ADX values, Daily date
        """
        endpoint = self.endpoints.adx
        key = AlphaVantage.adx
        filters = {AllowedDataFrameOperations.transpose: True}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df


class CalenderData:
    def __init__(self, endpoints: CalenderEndpoints):
        self.endpoints = endpoints

    @property
    def calender(self):
        endpoint = self.endpoints.company_earnings
        df = get_raw_api_csv_df(endpoint=endpoint)
        return df