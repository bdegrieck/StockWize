import pandas as pd
from typing import Any
from statsmodels.tsa.seasonal import MSTL
from statsmodels.tsa.stattools import acf, pacf
from BackEnd.Eda.helpers import CorrelationData, ConfidenceIntervalBounds
from BackEnd.constants import Finance


class MstlTerms:
    TREND = "trend"
    SEASONAL_7 = "seasonal_7"
    SEASONAL_30 = "seasonal_30"
    SEASONAL_365 = "seasonal_365"

def get_acf(df: pd.DataFrame, value_column: str, alpha: float = .05) -> CorrelationData:
    """
        Collect the acf data from the a dataframe and its value column

        Args:
            df: dataframe
            value_column: value column you want to get acf from
            alpha: default is 0.05 to set for confidence interval

        Returns:
            Correlation data of the coefficients of the lags and the lower and upper bounds of the acf plots
    """
    acf_coef = acf(x=df[value_column], alpha=alpha)
    acf_data = CorrelationData(
        coefficients=acf_coef[0],
        confidence_interval=ConfidenceIntervalBounds(
            lower_bound=acf_coef[1][:, 0],
            upper_bound=acf_coef[1][:, 1]
        )
    )
    return acf_data


def get_pacf(df: pd.DataFrame, value_column: str, alpha: float = .05) -> CorrelationData:
    """
    Collect the pacf data from the a dataframe and its value column

    Args:
        df: dataframe
        value_column: value column you want to get pacf from
        alpha: default is 0.05 to set for confidence interval

    Returns:
        Correlation data of the coefficients of the lags and the lower and upper bounds of the pacf plots
    """
    pacf_coef = pacf(x=df[value_column], alpha=alpha)
    pacf_data = CorrelationData(
        coefficients=pacf_coef[0],
        confidence_interval=ConfidenceIntervalBounds(
            lower_bound=pacf_coef[1][:, 0],
            upper_bound=pacf_coef[1][:, 1]
        )
    )
    return pacf_data


class Eda:

    def __init__(self, time_series_data: pd.DataFrame, ticker: str):
        self.time_series_data = time_series_data
        self.ticker = ticker

    def mstl(self, value_column: str) -> dict[str, Any]:
        """

        Args:
            value_column: value column of the df you want to do mstl on

        Returns:
            figure of the mstl plots. Returns the seasonal 7, 30, 365 plot and the trend
        """
        periods = [7, 30, 365]
        model = MSTL(self.time_series_data[value_column], periods=periods).fit()

        data = {
            Finance.date: self.time_series_data[Finance.date],
            MstlTerms.TREND: model.trend,
            MstlTerms.SEASONAL_7: model.seasonal.get(MstlTerms.SEASONAL_7),
            MstlTerms.SEASONAL_30: model.seasonal.get(MstlTerms.SEASONAL_30),
            MstlTerms.SEASONAL_365: model.seasonal.get(MstlTerms.SEASONAL_365)
        }
        data = {k: v for k, v in data.items() if v is not None}

        return data
