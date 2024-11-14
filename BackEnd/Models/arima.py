import pandas as pd
from pydantic.v1 import BaseModel, validator, Field
from statsmodels.tsa.arima.model import ARIMA

from BackEnd.Data.base import StringEnum
from BackEnd.Eda.eda import get_acf, get_pacf
from BackEnd.Eda.helpers import CorrelationData
from BackEnd.constants import Inequality, Finance
from BackEnd.error import ShapeError


class Trend(StringEnum):
    constant = "c"
    linear = "t"
    constant_trend = "ct"
    no_trend = "n"

class ForecastField(BaseModel):
    days: int = Field(gt=0, le=30)

class ArimaConfig(BaseModel):
    data: pd.Series
    q: int
    p: int
    d: int
    trend: Trend

    class Config:
        arbitrary_types_allowed = True

    @validator("data")
    def data_length(cls, data):
        if len(data) > 1000:
            raise ShapeError(inputted_size=len(data), allowed_size=1000, inequality=Inequality.lt_equal_to)
        return data


class Arima:

    def __init__(
            self,
            time_series: pd.DataFrame,
            value_column: str,
            date_column: str,
            diff=1
    ):
        self.df = time_series
        self.diff = diff
        self.value_column = value_column
        self.date_column = date_column
        self.max_date = None

    def fit(self) -> None:
        """
        Fit the Arima model

        Returns:
            None
        """
        df = self.df
        df[self.date_column] = pd.to_datetime(df[self.date_column])
        self.max_date = df[Finance.date].max()
        df = df.sort_values(by=self.date_column, ascending=True)

        if len(df) > 1000:
            df = df.iloc[-1000:]

        ar_lags = get_pacf(df=df, value_column=self.value_column, alpha=0.05)
        ma_lags = get_acf(df=df, value_column=self.value_column, alpha=0.05)
        sig_lags_ar = Arima._get_significant_lags(correlation_data=ar_lags)
        sig_lags_ma = Arima._get_significant_lags(correlation_data=ma_lags)

        if len(sig_lags_ma) == 0:
            p = 0
        else:
            p = max(sig_lags_ma)

        if len(sig_lags_ar) == 0:
            q = 0
        else:
            q = max(sig_lags_ar)

        trend = Trend.no_trend
        configurations = ArimaConfig(
            p=p,
            d=1,
            q=q,
            data=df[self.value_column],
            trend=trend
        )
        order = (configurations.p, configurations.d, configurations.q)
        self.model = ARIMA(
            endog=configurations.data,
            order=order,
            trend=configurations.trend
        )
        self.model = self.model.fit()

    def predict(self, steps: ForecastField) -> pd.DataFrame:
        """
        Forecasts a series of data

        Args:
            steps: Number of lags you want to forecast

        Returns:
            forecast (pd.DataFrame): DataFrame of the forecasted series with forecast values and forecasted dates
        """
        forecast_df = pd.DataFrame()
        forecast_df[Finance.date] = pd.date_range(start=self.max_date, periods=steps.days, freq="B").strftime(date_format='%Y-%m-%d')
        forecast_df[Finance.forecast] = self.model.forecast(steps=steps.days).values
        forecast_df.reset_index(inplace=True, drop=True)
        return forecast_df

    @staticmethod
    def _get_significant_lags(correlation_data: CorrelationData) -> list[int]:
        """
        Args:
            correlation_data: Coefficients and confidence intervals from acf and pacf calculations

        Returns:
            Significant lags where the coefficients are greater or less that the confidence intervals
        """
        significant_lags = []
        for lag in range(len(correlation_data.coefficients)):
            if correlation_data.coefficients[lag] > correlation_data.confidence_interval.upper_bound[lag] - correlation_data.coefficients[lag]:
                significant_lags.append(lag)
            elif correlation_data.coefficients[lag] < correlation_data.confidence_interval.lower_bound[lag] - correlation_data.coefficients[lag]:
                significant_lags.append(lag)
        return significant_lags
