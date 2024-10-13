import pandas as pd
from statsmodels.tsa.seasonal import MSTL
from BackEnd.plot import plot, Graph



class Eda:

    def __init__(self, time_series_data: pd.DataFrame, ticker: str):
        self.time_series_data = time_series_data
        self.ticker = ticker

    @property
    def mstl(self, value_column: str):
        periods = [7, 30, 365]
        model = MSTL(self.time_series_data[value_column], periods=periods).fit()

        trend = model.trend
        seasonal_7 = model.seasonal["seasonal_7"]
        seasonal_30 = model.seasonal["seasonal_30"]
        seasonal_365 = model.seasonal["seasonal_365"]

        graphs = [
            Graph(
                xaxis_data=pd.Series(trend.index),
                yaxis_data=trend,
                x_title="Date",
                y_title="Trend",
                title="Trend stock"
            ),
            Graph(
                xaxis_data=pd.Series(seasonal_7.index),
                yaxis_data=seasonal_7,
                x_title="Date",
                y_title="Seasonal 7",
                title="Seasonal Weekly"
            ),
            Graph(
                xaxis_data=pd.Series(seasonal_30.index),
                yaxis_data=seasonal_30,
                x_title="Date",
                y_title="Seasonal 30",
                title="Seasonal Monthly"
            ),
            Graph(
                xaxis_data=pd.Series(seasonal_365.index),
                yaxis_data=seasonal_365,
                x_title="Date",
                y_title="Seasonal 365",
                title="Seasonal Yearly"
            )
        ]

        main_title = f"Closing Prices MSTL of {self.ticker}"
        fig = plot(graphs=graphs, main_title=main_title)

        return fig
