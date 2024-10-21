from typing import Any

from pydantic.v1 import validator, BaseModel

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


def get_ticker_symbol_from_keyword(keyword_data: dict[str, Any]) -> str:
    """
    Method to get a ticker symbol from a dictionary of keyword matches from the api

    Args:
        keyword_data (dict[str, Any]): dictionary of a list of tickers that are most relevant to the keyword
    Returns:
        ticker (str): ticker of the closest match
    """
    try:
        matches = keyword_data.get("bestMatches")
        for match in matches:
            meta_data = ValidTickerType(currency=match.get("8. currency"), region=match.get("4. region"), ticker=match.get("1. symbol"))
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
