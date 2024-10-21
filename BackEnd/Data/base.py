from abc import ABC, abstractmethod
from enum import Enum

class Company(ABC):

    @abstractmethod
    def time_series(self):
        """
        Open, High, Low, Close, Volume, Dividend
        """
        pass

    @abstractmethod
    def overview(self):
        """
        Symbol, Company name, Description of Company, Year high of the stock, Year low of the stock
        """
        pass

    @abstractmethod
    def income_statement(self):
        """
        Quarter dates, Total revenue quarterly, profit quarterly
        """
        pass

    @abstractmethod
    def cash_flow(self):
        """
        Quarter dates, operating cashflow quarterly, financing cash flow quarterly, from investment cash flow quarterly
        """
        pass

    @abstractmethod
    def earnings(self):
        """
        Quarter dates, report dates quarterly, eps quarterly, estimated eps quarterly, surprise percentage quarterly
        """
        pass

    @abstractmethod
    def news(self):
        pass


class Micro(ABC):

    @abstractmethod
    def real_gdp(self):
        """
        Real GDP quarterly at the beginning of the year, Date quarterly
        """
        pass

    @abstractmethod
    def cpi(self):
        """
        Cpi value, first day of the monthly dates
        """
        pass

    @abstractmethod
    def inflation(self):
        """
        Inflation percentage per year, dates first day of the year
        """
        pass

    @abstractmethod
    def federal_funds_rate(self):
        """
        Federal funds rate monthly, first day of the month for dates
        """
        pass

    @abstractmethod
    def retail_sales(self):
        """
        Returns the retail sales in millions per month, date is first day of every month
        """
        pass

    @abstractmethod
    def unemployment_rate(self):
        """
        Unemployment rate at the beginning of the month
        """
        pass


class TechIndicators(ABC):

    @abstractmethod
    def sma(self):
        """
        SMA value, weekly date
        """
        pass

    @abstractmethod
    def ema(self):
        """
        EMA values, weekly date
        """
        pass

    @abstractmethod
    def rsi(self):
        """
        RSI values, weekly date
        """
        pass

    @abstractmethod
    def bbands(self):
        """
        Bbands values, weekly date
        """
        pass

    @abstractmethod
    def adx(self):
        """
        ADX values, Daily date
        """
        pass

class StringEnum(str, Enum):
    """
    String Enum class
    """
    pass


class StockWizeException(Exception, ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @property
    @abstractmethod
    def message(self):
        """
        Returns the message of the error raised
        """
        pass
