from typing import Optional

import requests
from pydantic.v1 import validator, BaseModel

from BackEnd.constants import AlphaVantage, API_KEY
from BackEnd.error import TickerError


class AllowedTickerType:
    currency = "USD"
    region = "United States"
    invalid_char= "."


class ValidTickerType(BaseModel):
    currency: Optional[str] = None
    region: Optional[str] = None
    ticker: Optional[str] = None # Keeps track of overall validity
    valid: bool = True

    @validator("currency", "region", "ticker", pre=True, each_item=True)
    def validate_ticker(cls, v, field):
        if field.name == "region" and v != AllowedTickerType.region:
            return None

        if field.name == "ticker" and AllowedTickerType.invalid_char in v:
            return None

        if field.name == "currency" and v != AllowedTickerType.currency:
            return None

        return v

    def __post_init__(self):
        # If any field is None due to validation, mark as invalid
        if not all([self.currency, self.region, self.ticker]):
            self.valid = False


def check_extraneous_tickers(input_name: str):
    """
    Args:
    input_name (str): Checks if input company name from the user is in the extraneous ticker dict. Alpha vantage does
    not correctly match keywords with tickers. An example would be for Apple alpha vantage wouldn't return AAPL
    """
    extraneous_tickers = {
        "apple": "AAPL",
        "target": "TGT",
        "google": "GOOGL",
        "disney": "DIS",
        "at&t": "T",
        "visa": "V",
        "berkshire hathaway": "BRK",
        "eli lily & co": "LLY",
        "eli lily and co": "LLY",
        "eli lily": "LLY",
        "chase": "JPM",
        "jpmorgan": "JPM",
        "johnson & johnson": "JNJ",
        "johnson and johnson": "JNJ",
        "coca cola": "KO",
        "mcdonalds": "MCD",
        "microsoft": "MSFT",
        "ford": "F"
    }
    if input_name in extraneous_tickers.keys():
        return extraneous_tickers[input_name]


def validate_ticker(symbol: str) -> str:
    """
    Method to get a ticker symbol from a dictionary of keyword matches from the api

    Args:
        symbol (str): Input from the user
    Returns:
        ticker (str): ticker of the closest match
    """
    symbol = symbol.lower()
    extraneous_ticker = check_extraneous_tickers(input_name=symbol)
    if extraneous_ticker is not None:
        return extraneous_ticker

    endpoint = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={API_KEY}'
    response = requests.get(endpoint)
    keyword_data = response.json()
    matches = keyword_data.get(AlphaVantage.best_matches)
    for match in matches:
        meta_data = ValidTickerType(
            currency=match.get(AlphaVantage.currency),
            region=match.get(AlphaVantage.region),
            ticker=match.get(AlphaVantage.symbol)
        )
        if meta_data is not None:
            ticker = meta_data.ticker
            return ticker

    # If a ticker isn't returned
    raise TickerError(input=symbol)

