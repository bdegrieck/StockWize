from BackEnd.Data.base import StockWizeException
from BackEnd.constants import Inequality


class TickerError(Exception):
    def __init__(self, input: str):
        self.input = input

    def __str__(self):
        return self.message

    @property
    def message(self):
        return f"Invalid input: {self.input}"


class EndpointError(StockWizeException):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def __str__(self):
        return self.message

    @property
    def message(self):
        return f"Error connecting with endpoint: {self.endpoint}"

class ColumnError(StockWizeException):
    def __init__(self, error_column: str, allowed_columns: str):
        self.error_column = error_column
        self.allowed_columns = allowed_columns

    def __str__(self):
        return self.message

    @property
    def message(self):
        return f"Invalid column: {self.error_column}, allowed columns are: {self.allowed_columns}"


class ShapeError(StockWizeException):
    def __init__(self, inputted_size: int, allowed_size: int, inequality: Inequality):
        self.inputted_size = inputted_size
        self.allowed_size = allowed_size
        self.inequality = inequality

    def __str__(self):
        return self.message

    @property
    def message(self):
        return f"Invalid size inputted: {self.inputted_size}, allowed size is {self.inequality}: {self.allowed_size}"
