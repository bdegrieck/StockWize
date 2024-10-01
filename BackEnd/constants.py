API_KEY = "CRU63X7J4COJ46F2"


class AlphaVantage:
    quarterly_reports_dict = "quarterlyReports"
    time_series_dict = "Time Series (Daily)"
    quarterly_earnings_dict = "quarterlyEarnings"
    feed = "feed"

class Finance:
    fiscal_dates = "fiscalDateEnding"
    report_dates = "reportedDate"
    total_revenue = "totalRevenue"
    profit = "netIncome"
    symbol = "Symbol"
    name = "Name"
    description = "Description"
    year_high = "52WeekHigh"
    year_low = "52WeekLow"
    open = "Open"
    high = "High"
    low = "Low"
    non_adjust_close = "NonAdjustClose"
    close = "Close"
    volume = "Volume"
    dividend = "Dividend"
    split = "Split"
    operating_cash_flow = "operatingCashflow"
    from_investment_cash_flow = "cashflowFromInvestment"
    from_financing_cash_flow = "cashflowFromFinancing"
    reported_eps = "reportedEPS"
    estimated_eps = "estimatedEPS"
    surprise_percentage = "surprisePercentage"


class AllowedDataFrameOperations:
    """
    Allowed df operations
    transpose - transposing the df
    columns - grabbing certain columns from a df. Can be one or multiple
    rename - ranaming columns
    drop - droping certain columns
    """
    transpose = "transpose"
    columns = "columns"
    drop = "drop columns"
    rename = "rename"
