from BackEnd.base import Company, Micro, TechIndicators
from BackEnd.constants import API_KEY


class CompanyEndpoints(Company):

    def __init__(self, ticker: str):
        self.ticker = ticker

    @property
    def time_series(self):
        return f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={self.ticker}&apikey={API_KEY}&outputsize=full&datatype=json'

    @property
    def overview(self):
        return f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.ticker}&apikey={API_KEY}&outputsize=full&datatype=json'

    @property
    def income_statement(self):
        return f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.ticker}&apikey={API_KEY}&datatype=json'

    @property
    def cash_flow(self):
        return f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={self.ticker}&apikey={API_KEY}&datatype=json'

    @property
    def earnings(self):
        return f'https://www.alphavantage.co/query?function=EARNINGS&symbol={self.ticker}&apikey={API_KEY}'

    @property
    def news(self):
        return f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={self.ticker}&apikey={API_KEY}&datatype=json'

class ValidationEndpoints:

    def __init__(self, keyword: str):
        self.keyword = keyword

    @property
    def ticker_search(self):
        return f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={self.keyword}&apikey={API_KEY}datatype=json'

class MicroEndpoints(Micro):

    @property
    def real_gdp(self):
        return f"https://www.alphavantage.co/query?function=REAL_GDP&symbol=AAPL&apikey={API_KEY}&datatype=json&interval=quarterly"

    @property
    def cpi(self):
        return f"https://www.alphavantage.co/query?function=CPI&symbol=AAPL&apikey={API_KEY}&datatype=json"

    @property
    def inflation(self):
        return f"https://www.alphavantage.co/query?function=INFLATION&symbol=AAPL&apikey={API_KEY}&datatype=json"

    @property
    def federal_funds_rate(self):
        return f"https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&symbol=AAPL&apikey={API_KEY}&datatype=json"

    @property
    def retail_sales(self):
        return f"https://www.alphavantage.co/query?function=RETAIL_SALES&symbol=AAPL&apikey={API_KEY}&datatype=json"

    @property
    def unemployment_rate(self):
        return f"https://www.alphavantage.co/query?function=UNEMPLOYMENT&symbol=AAPL&apikey={API_KEY}&datatype=json"


class CalenderEndpoints:

    def __init__(self, ticker: str):
        self.ticker = ticker

    @property
    def upcoming_earnings(self):
        """
            Return: Upcmoing earnings forecasted in 3 months for any company
        """
        return f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={API_KEY}&datatype=json"

    @property
    def company_earnings(self):
        """
            Return: Upcoming Earnings for a company for the year
        """
        return f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol={self.ticker}&horizon=12month&apikey={API_KEY}"


class TechIndEndpoints(TechIndicators):

    def __init__(self, ticker: str):
        self.ticker = ticker

    @property
    def sma(self):
        return f'https://www.alphavantage.co/query?function=SMA&symbol={self.ticker}&interval=weekly&time_period=10&series_type=open&apikey={API_KEY}&datatype=json'

    @property
    def ema(self):
        return f'https://www.alphavantage.co/query?function=EMA&symbol={self.ticker}&interval=weekly&time_period=10&series_type=open&apikey={API_KEY}&datatype=json'

    @property
    def rsi(self):
        return f'https://www.alphavantage.co/query?function=RSI&symbol={self.ticker}&interval=weekly&time_period=10&series_type=open&apikey={API_KEY}&datatype=json'

    @property
    def bbands(self):
        return f'https://www.alphavantage.co/query?function=BBANDS&symbol={self.ticker}&interval=weekly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey={API_KEY}&datatype=json'

    @property
    def adx(self):
        return f'https://www.alphavantage.co/query?function=ADX&symbol={self.ticker}&interval=daily&time_period=10&apikey={API_KEY}&datatype=json'
