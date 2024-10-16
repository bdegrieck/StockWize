import pandas as pd
from statsmodels.tsa.seasonal import MSTL
from statsmodels.tsa.stattools import acf, pacf

from BackEnd.Eda.helpers import CorrelationData, ConfidenceIntervalBounds
from BackEnd.Eda.plot import plot, MSTLGraph
from BackEnd.constants import Finance


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
            MSTLGraph(
                xaxis_data=pd.Series(trend.index),
                yaxis_data=trend,
                x_title="Date",
                y_title="Trend",
                title="Trend stock"
            ),
            MSTLGraph(
                xaxis_data=pd.Series(seasonal_7.index),
                yaxis_data=seasonal_7,
                x_title="Date",
                y_title="Seasonal 7",
                title="Seasonal Weekly"
            ),
            MSTLGraph(
                xaxis_data=pd.Series(seasonal_30.index),
                yaxis_data=seasonal_30,
                x_title="Date",
                y_title="Seasonal 30",
                title="Seasonal Monthly"
            ),
            MSTLGraph(
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

    @property
    def acf(self) -> CorrelationData:
        acf_coef = acf(self.time_series_data[Finance.close], alpha=.05)
        acf_data = CorrelationData(
            coefficients=acf_coef[0],
            confidence_interval=ConfidenceIntervalBounds(
                lower_bound=acf_coef[1][:, 0],
                upper_bound=acf_coef[1][:, 1]
            )
        )
        return acf_data

    @property
    def pacf(self) -> CorrelationData:
        pacf_coef = pacf(self.time_series_data[Finance.close], alpha=.05)
        pacf_data = CorrelationData(
            coefficients=pacf_coef[0],
            confidence_interval=ConfidenceIntervalBounds(
                lower_bound=pacf_coef[1][:, 0],
                upper_bound=pacf_coef[1][:, 1]
            )
        )
        return pacf_data
