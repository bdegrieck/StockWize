from typing import Any

import requests
from pydantic.v1 import validator, BaseModel

from BackEnd.constants import AlphaVantage, API_KEY
from BackEnd.error import TickerError


class AllowedTickerType:
    currency = "USD"
    region = "United States"
    invalid_char= "."


class ValidTickerType(BaseModel):
    currency: str   # currency of stock ex: USD
    region: str     # country of the stock ex: United States
    ticker: str    # inputted keyword

    @validator("currency", "region", "ticker")
    def validate_ticker(cls, currency, region, ticker):
        if region != AllowedTickerType.region:
            message = f"Your input: {ticker} is not supported because it is a foreign stock in region {region}"
            raise TickerError(msg=message)

        if AllowedTickerType.invalid_char in ticker:
            message = f"Your input: {ticker} is not supported because it is a foreign stock symbol {AllowedTickerType.invalid_char}"
            raise TickerError(msg=message)

        if currency != AllowedTickerType.currency:
            message = f"Your input: {ticker} is not supported because it is a foreign stock with currency {currency}"
            raise TickerError(msg=message)


def validate_ticker(symbol: str) -> str:
    """
    Method to get a ticker symbol from a dictionary of keyword matches from the api

    Args:
        input (str): Input from the user
    Returns:
        ticker (str): ticker of the closest match
    """
    endpoint = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={API_KEY}datatype=json'
    response = requests.get(endpoint)
    keyword_data = response.json()
    try:
        matches = keyword_data.get(AlphaVantage.best_matches)
        for match in matches:
            meta_data = ValidTickerType(
                currency=match.get(AlphaVantage.currency),
                region=match.get(AlphaVantage.region),
                ticker=match.get(AlphaVantage.symbol)
            )
            ticker = meta_data.ticker
            return ticker
    except TickerError as e:
        return f"Error: {e.message}"


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
    }
    if input_name in extraneous_tickers.keys():
        return extraneous_tickers[input_name]
