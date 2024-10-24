from typing import Dict
import pandas as pd
from Data.endpoints import CompanyEndpoints, get_raw_data
from BackEnd.constants import Finance

class TickerComparison:
    
    def __init__(self, ticker1: str, ticker2: str):
        self.ticker1 = ticker1
        self.ticker2 = ticker2

    def fetch_company_data(self, ticker: str) -> pd.DataFrame:
        """
        Fetch and return the required data for comparison for a given ticker as a DataFrame.
        """
        endpoints = CompanyEndpoints(ticker)
        overview_data = get_raw_data(endpoints.overview, {})
        time_series_data = get_raw_data(endpoints.time_series, {})
        income_statement_data = get_raw_data(endpoints.income_statement, {})

        # Extract relevant metrics
        market_cap = float(overview_data.get("MarketCapitalization", "0").replace(",", ""))
        eps = float(overview_data.get("EPS", 0))
        latest_date = max(time_series_data[Finance.time_series_dict].keys())
        stock_price = float(time_series_data[Finance.time_series_dict][latest_date][Finance.close])
        
        # Extract financial data
        annual_reports = income_statement_data.get(Finance.quarterly_reports_dict, [])
        
        if annual_reports:
            latest_report = annual_reports[0]  # Assume sorted by fiscal year
            revenue = float(latest_report.get(Finance.total_revenue, 0).replace(",", ""))
            profit = float(latest_report.get(Finance.profit, 0).replace(",", ""))
        else:
            revenue = 0
            profit = 0

        # Calculate price per earnings (PPE)
        ppe = stock_price / eps if eps else 0

        # Convert to DataFrame
        data = {
            Finance.market_cap: [market_cap],
            Finance.close: [stock_price],
            Finance.reported_eps: [eps],
            Finance.total_revenue: [revenue],
            Finance.profit: [profit],
            "ppe": [ppe]
        }

        return pd.DataFrame(data)

    def compare_tickers(self) -> pd.DataFrame:
        """
        Fetch data for both tickers and provide a comparison using DataFrames.
        """
        data_ticker1 = self.fetch_company_data(self.ticker1)
        data_ticker2 = self.fetch_company_data(self.ticker2)

        # Calculate differences and round the values for consistency
        difference = {
            Finance.market_cap: round(data_ticker1[Finance.market_cap].iloc[0] - data_ticker2[Finance.market_cap].iloc[0], 2),
            Finance.close: round(data_ticker1[Finance.close].iloc[0] - data_ticker2[Finance.close].iloc[0], 2),
            Finance.reported_eps: round(data_ticker1[Finance.reported_eps].iloc[0] - data_ticker2[Finance.reported_eps].iloc[0], 2),
            Finance.total_revenue: round(data_ticker1[Finance.total_revenue].iloc[0] - data_ticker2[Finance.total_revenue].iloc[0], 2),
            Finance.profit: round(data_ticker1[Finance.profit].iloc[0] - data_ticker2[Finance.profit].iloc[0], 2),
            "ppe": round(data_ticker1["ppe"].iloc[0] - data_ticker2["ppe"].iloc[0], 2)
        }

        # Combine into a DataFrame
        comparison_df = pd.DataFrame({
            "Ticker1": data_ticker1.iloc[0],
            "Ticker2": data_ticker2.iloc[0],
            "Difference": difference
        })

        return comparison_df
