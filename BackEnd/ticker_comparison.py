from typing import Dict
from BackEnd.api import CompanyEndpoints, get_raw_data

class TickerComparison:
    
    def __init__(self, ticker1: str, ticker2: str):
        self.ticker1 = ticker1
        self.ticker2 = ticker2

    def fetch_company_data(self, ticker: str) -> Dict[str, float]:
        """
        Fetch and return the required data for comparison for a given ticker.
        """
        endpoints = CompanyEndpoints(ticker)
        overview_data = get_raw_data(endpoints.overview, {})
        time_series_data = get_raw_data(endpoints.time_series, {})

        # Debugging: Print the raw data for better inspection
        print(f"Overview Data for {ticker}: {overview_data}")
        print(f"Time Series Data for {ticker}: {time_series_data}")
        
        # Extract relevant metrics
        market_cap = float(overview_data.get("MarketCapitalization", "0").replace(",", ""))
        eps = float(overview_data.get("EPS", 0))
        latest_date = max(time_series_data["Time Series (Daily)"].keys())
        stock_price = float(time_series_data["Time Series (Daily)"][latest_date]["4. close"])
        
        # Extract financial data
        income_statement_data = get_raw_data(endpoints.income_statement, {})
        annual_reports = income_statement_data.get("annualReports", [])
        print(f"Income Statement Data for {ticker}: {income_statement_data}")

        if annual_reports:
            latest_report = annual_reports[0]  # Assume sorted by fiscal year
            revenue = float(latest_report.get("totalRevenue", 0).replace(",", ""))
            profit = float(latest_report.get("netIncome", 0).replace(",", ""))
        else:
            revenue = 0
            profit = 0

        # Calculate price per earnings (PPE)
        ppe = stock_price / eps if eps else 0

        return {
            "market_cap": market_cap,
            "stock_price": stock_price,
            "eps": eps,
            "revenue": revenue,
            "profit": profit,
            "ppe": ppe
        }

    def compare_tickers(self) -> Dict[str, Dict[str, float]]:
        """
        Fetch data for both tickers and provide a comparison.
        """
        data_ticker1 = self.fetch_company_data(self.ticker1)
        data_ticker2 = self.fetch_company_data(self.ticker2)

        print(f"Data for {self.ticker1}: {data_ticker1}")
        print(f"Data for {self.ticker2}: {data_ticker2}")
        
        comparison = {
            "ticker1": data_ticker1,
            "ticker2": data_ticker2,
            "difference": {
                "market_cap": data_ticker1["market_cap"] - data_ticker2["market_cap"],
                "stock_price": data_ticker1["stock_price"] - data_ticker2["stock_price"],
                "eps": data_ticker1["eps"] - data_ticker2["eps"],
                "revenue": data_ticker1["revenue"] - data_ticker2["revenue"],
                "profit": data_ticker1["profit"] - data_ticker2["profit"],
                "ppe": data_ticker1["ppe"] - data_ticker2["ppe"]
            }
        }
        
        return comparison
