import numpy as np
import pandas as pd
from typing import Any

from BackEnd.Data.endpoints import CompanyEndpoints, MicroEndpoints, TechIndEndpoints, CalenderEndpoints
from BackEnd.Data.helpers import get_data_df, get_raw_api_csv_df, format_df
from BackEnd.News.news import News
from BackEnd.constants import Finance, AlphaVantage, AllowedOrientations, MicroEconomic, TechnicalIndicators

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file into the environment


class CompanyData(CompanyEndpoints):

    def __init__(self, ticker: str):
        super().__init__(ticker)

    @property
    def time_series(self) -> pd.DataFrame:
        endpoint = super().time_series
        key = AlphaVantage.time_series_dict
        columns = [
            Finance.date,
            Finance.open,
            Finance.high,
            Finance.low,
            Finance.close,
            Finance.volume,
            Finance.dividend,
        ]

        renamed_columns = {
            "index": Finance.date,
            "1. open": Finance.open,
            "2. high": Finance.high,
            "3. low": Finance.low,
            "4. close": Finance.non_adjust_close,
            "5. adjusted close": Finance.close,
            "6. volume": Finance.volume,
            "7. dividend amount": Finance.dividend,
        }
        df = get_data_df(endpoint=endpoint, key=key, orient=AllowedOrientations.index)
        df.reset_index(inplace=True, names=Finance.date)
        df = format_df(df=df)
        df.rename(columns=renamed_columns, inplace=True)
        df = df[columns]
        return df

    @property
    def overview(self) -> pd.DataFrame:
        endpoint = super().overview
        columns = [Finance.symbol, Finance.name, Finance.description, Finance.year_high, Finance.year_low, Finance.market_cap]
        df = get_data_df(endpoint=endpoint)
        df = format_df(df=df)
        df = df[columns]
        return df

    @property
    def income_statement(self) -> pd.DataFrame:
        endpoint = super().income_statement
        columns = [Finance.fiscal_dates, Finance.total_revenue, Finance.profit]
        key = AlphaVantage.quarterly_reports_dict
        df = get_data_df(endpoint=endpoint, key=key)
        df = format_df(df=df)
        df = df[columns]
        return df

    @property
    def cash_flow(self) -> pd.DataFrame:
        endpoint = super().cash_flow
        key = AlphaVantage.quarterly_reports_dict
        columns = [Finance.fiscal_dates, Finance.operating_cash_flow, Finance.from_financing_cash_flow, Finance.from_investment_cash_flow]
        df = get_data_df(endpoint=endpoint, key=key)
        df = format_df(df=df)
        df = df[columns]
        return df

    @property
    def earnings(self) -> pd.DataFrame:
        endpoint = super().earnings
        key = AlphaVantage.quarterly_earnings_dict
        columns = [Finance.fiscal_dates, Finance.report_dates, Finance.reported_eps, Finance.estimated_eps, Finance.surprise_percentage]
        df = get_data_df(endpoint=endpoint, key=key)
        df = format_df(df=df)
        df = df[columns]
        return df

    @property
    def news(self) -> list[dict[str, Any]]:
        news_endpoint = super().news
        news_instance = News(ticker=self.ticker, endpoint=news_endpoint)
        return news_instance.get_news

class MicroData(MicroEndpoints):

    @property
    def real_gdp(self) -> pd.DataFrame:
        endpoint = super().real_gdp
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        columns_renamed = {"date": Finance.date, "value": MicroEconomic.real_gdp}
        df = df.rename(columns=columns_renamed)
        return df

    @property
    def cpi(self) -> pd.DataFrame:
        endpoint = super().cpi
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        columns_renamed = {"date": Finance.date, "value": MicroEconomic.cpi}
        df = df.rename(columns=columns_renamed)
        return df

    @property
    def inflation(self) -> pd.DataFrame:
        endpoint = super().inflation
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        columns_renamed = {"date": Finance.date, "value": MicroEconomic.inflation}
        df = df.rename(columns=columns_renamed)
        return df

    @property
    def federal_funds_rate(self) -> pd.DataFrame:
        endpoint = super().federal_funds_rate
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        columns_renamed = {"date": Finance.date, "value": MicroEconomic.interest_rates}
        df = df.rename(columns=columns_renamed)
        return df

    @property
    def retail_sales (self) -> pd.DataFrame:
        endpoint = super().retail_sales
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        columns_renamed = {"date": Finance.date, "value": MicroEconomic.retail_sales}
        df = df.rename(columns=columns_renamed)
        return df

    @property
    def unemployment_rate(self) -> pd.DataFrame:
        endpoint = super().unemployment_rate
        key = AlphaVantage.data
        df = get_data_df(endpoint=endpoint, key=key)
        columns_renamed = {"date": Finance.date, "value": MicroEconomic.unemployment_rate}
        df = df.rename(columns=columns_renamed)
        return df


class TechIndData(TechIndEndpoints):

    def __init__(self, ticker: str):
        super().__init__(ticker=ticker)

    @property
    def sma(self) -> pd.DataFrame:
        endpoint = super().sma
        key = AlphaVantage.sma
        orient = AllowedOrientations.index
        df = get_data_df(endpoint=endpoint, key=key, orient=orient)
        df.reset_index(inplace=True, names=Finance.date)
        df = format_df(df=df)
        columns_renamed = {"SMA": TechnicalIndicators.sma}
        df = df.rename(columns=columns_renamed)
        return df

    @property
    def ema(self) -> pd.DataFrame:
        endpoint = super().ema
        key = AlphaVantage.ema
        orient = AllowedOrientations.index
        df = get_data_df(endpoint=endpoint, key=key, orient=orient)
        df.reset_index(inplace=True, names=Finance.date)
        df = format_df(df=df)
        columns_renamed = {"EMA": TechnicalIndicators.ema}
        df = df.rename(columns=columns_renamed)
        return df

    @property
    def rsi(self) -> pd.DataFrame:
        endpoint = super().rsi
        key = AlphaVantage.rsi
        orient = AllowedOrientations.index
        df = get_data_df(endpoint=endpoint, key=key, orient=orient)
        df.reset_index(inplace=True, names=Finance.date)
        df = format_df(df=df)
        columns_renamed = {"RSI": TechnicalIndicators.rsi}
        df = df.rename(columns=columns_renamed)
        return df

    @property
    def bbands(self) -> pd.DataFrame:
        endpoint = super().bbands
        key = AlphaVantage.bbands
        orient = AllowedOrientations.index
        df = get_data_df(endpoint=endpoint, key=key, orient=orient)
        df.reset_index(inplace=True, names=Finance.date)
        df = format_df(df=df)
        columns_renamed = {
            "Real Upper Band": TechnicalIndicators.bbands_upper,
            "Real Middle Band": TechnicalIndicators.bbands_middle,
            "Real Lower Band": TechnicalIndicators.bbands_lower
        }
        df = df.rename(columns=columns_renamed)
        return df

    @property
    def adx(self) -> pd.DataFrame:
        endpoint = super().adx
        key = AlphaVantage.adx
        orient = AllowedOrientations.index
        df = get_data_df(endpoint=endpoint, key=key, orient=orient)
        df.reset_index(inplace=True, names=Finance.date)
        df = format_df(df=df)
        columns_renamed = {"ADX": TechnicalIndicators.adx}
        df = df.rename(columns=columns_renamed)
        return df


class ForecastData:
    def __init__(self, ticker: str):
        self.ticker = ticker

    def lstm(self, time_series: pd.DataFrame) -> pd.DataFrame:
        indicator_instance = TechIndData(ticker=self.ticker)
        df = (
            pd.merge(left=indicator_instance.bbands, right=indicator_instance.ema, on=Finance.date
            ).merge(right=indicator_instance.rsi, on=Finance.date
            ).merge(right=indicator_instance.sma, on=Finance.date
            ).merge(right=indicator_instance.adx, how="outer"
            ).merge(right=time_series[[Finance.date, Finance.close]], on=Finance.date)
        )
        df = df.fillna(method='ffill').dropna().reset_index(drop=True)
        df = df.reset_index(drop=False, names="Count")
        df["ID"] = "1"
        return df


class CalenderData:
    def __init__(self, endpoints: CalenderEndpoints):
        self.endpoints = endpoints

    @property
    def calender(self):
        endpoint = self.endpoints.company_earnings
        df = get_raw_api_csv_df(endpoint=endpoint)
        return df
