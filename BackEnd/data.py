import pandas as pd

from BackEnd.base import Micro, TechIndicators
from BackEnd.endpoints import CompanyEndpoints, MicroEndpoints, TechIndEndpoints, CalenderEndpoints
from BackEnd.constants import Finance, AlphaVantage, AllowedDataFrameOperations
from BackEnd.helpers import get_data_df, get_raw_api_csv_df
from BackEnd.news import News


class CompanyData(CompanyEndpoints):

    def __init__(self, ticker: str):
        super().__init__(ticker)

    @property
    def time_series(self) -> pd.DataFrame:
        endpoint = super().time_series
        key = AlphaVantage.time_series_dict
        columns = [
            Finance.open,
            Finance.high,
            Finance.low,
            Finance.non_adjust_close,
            Finance.close,
            Finance.volume,
            Finance.dividend,
        ]

        renamed_columns = {
            "1. open": Finance.open,
            "2. high": Finance.high,
            "3. low": Finance.low,
            "4. close": Finance.non_adjust_close,
            "5. adjusted close": Finance.close,
            "6. volume": Finance.volume,
            "7. dividend amount": Finance.dividend,
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
        endpoint = super().overview
        columns = [Finance.symbol, Finance.name, Finance.description, Finance.year_high, Finance.year_low]
        filters = {AllowedDataFrameOperations.columns: columns}
        df = get_data_df(endpoint=endpoint, filters=filters)
        return df

    @property
    def income_statement(self) -> pd.DataFrame:
        endpoint = super().income_statement
        columns = [Finance.fiscal_dates, Finance.total_revenue, Finance.profit]
        filters = {AllowedDataFrameOperations.columns: columns}
        key = AlphaVantage.quarterly_reports_dict
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def cash_flow(self) -> pd.DataFrame:
        endpoint = super().cash_flow
        key = AlphaVantage.quarterly_reports_dict
        columns = [Finance.fiscal_dates, Finance.operating_cash_flow, Finance.from_financing_cash_flow, Finance.from_investment_cash_flow]
        filters = {AllowedDataFrameOperations.columns: columns}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def earnings(self) -> pd.DataFrame:
        endpoint = super().earnings
        key = AlphaVantage.quarterly_earnings_dict
        columns = [Finance.fiscal_dates, Finance.report_dates, Finance.reported_eps, Finance.estimated_eps, Finance.surprise_percentage]
        filters = {AllowedDataFrameOperations.columns: columns}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def news(self) -> str:
        news_instance = News(ticker=self.ticker, endpoint=super().news)
        return news_instance.get_news

class MicroData(MicroEndpoints):

    @property
    def real_gdp(self) -> pd.DataFrame:
        endpoint = super().real_gdp
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df

    @property
    def cpi(self) -> pd.DataFrame:
        endpoint = super().cpi
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df

    @property
    def inflation(self) -> pd.DataFrame:
        endpoint = super().inflation
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df

    @property
    def federal_funds_rate(self) -> pd.DataFrame:
        endpoint = super().federal_funds_rate
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df

    @property
    def retail_sales (self) -> pd.DataFrame:
        endpoint = super().retail_sales
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df

    @property
    def unemployment_rate(self) -> pd.DataFrame:
        endpoint = super().unemployment_rate
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        return df


class TechIndData(TechIndEndpoints):

    def __init__(self, ticker: str):
        super().__init__(ticker=ticker)

    @property
    def sma(self) -> pd.DataFrame:
        endpoint = super().sma
        key = AlphaVantage.sma
        filters = {AllowedDataFrameOperations.transpose: True}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def ema(self) -> pd.DataFrame:
        endpoint = super().ema
        key = AlphaVantage.ema
        filters = {AllowedDataFrameOperations.transpose: True}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def rsi(self) -> pd.DataFrame:
        endpoint = super().rsi
        key = AlphaVantage.rsi
        filters = {AllowedDataFrameOperations.transpose: True}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def bbands(self) -> pd.DataFrame:
        endpoint = super().bbands
        key = AlphaVantage.bbands
        filters = {AllowedDataFrameOperations.transpose: True}
        df = get_data_df(endpoint=endpoint, key=key, filters=filters)
        return df

    @property
    def adx(self) -> pd.DataFrame:
        endpoint = super().adx
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