
class TickerError(Exception):
    def __init__(self, msg: str):
        self.message = msg
        super().__init__(self.message)


class EndpointError(Exception):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def __str__(self):
        return self.message

    @property
    def message(self):
        return f"Error connecting with endpoint: {self.endpoint}"

class ColumnError(Exception):
    def __init__(self, error_column: str, allowed_columns: str):
        self.error_column = error_column
        self.allowed_columns = allowed_columns

    def __str__(self):
        return self.message

    @property
    def message(self):
        return f"Invalid column: {self.error_column}, allowed columns are: {self.allowed_columns}"

