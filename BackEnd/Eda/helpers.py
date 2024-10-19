import numpy as np
from pydantic import BaseModel
from pydantic.v1 import validator

from BackEnd.constants import Inequality
from BackEnd.error import ShapeError

class ConfidenceIntervalBounds(BaseModel):
    """
    lower_bounds: lower bounds of the coefficients
    upper_bounds: upper bounds of the coefficients
    """
    lower_bound: np.array
    upper_bound: np.array

    @validator("lower_bound", "upper_bound")
    def check_bounds_ndim(cls, bounds):
        if bounds.ndim != 1:
            raise ShapeError(inputted_size=bounds.ndim, allowed_size=1, inequality=Inequality.equal)
        return bounds

    class Config:
        arbitrary_types_allowed = True

class CorrelationData(BaseModel):
    """
    coefficients: Coefficients of the auto correlation models
    confidence_intervals: confidence intervals of the coefficients
    """
    coefficients: np.array
    confidence_interval: ConfidenceIntervalBounds

    @validator("coefficients")
    def check_confidence_interval_shape(cls, coef):
        if coef.ndim != 1:
            raise ShapeError(inputted_size=coef.ndim, allowed_size=1, inequality=Inequality.equal)
        return coef

    class Config:
        arbitrary_types_allowed = True


def get_significant_lags(coef: CorrelationData) -> list[int]:
    """
    Gets the significant lags that are greater than the upper bounds or lower than the lower bounds
    Args:
        coef (CorrelationData) - Correlation coefficients along with upper and lower bounds

    Returns:
        sig_lags (list[int]): list of the significant lags
    """
    sig_lags = []
    for i in range(1, len(coef.coefficients)):
        if coef.coefficients[i] > (coef.confidence_interval.upper_bound[i] - coef.coefficients[i]):
            sig_lags.append(i)
        elif coef.coefficients[i] < (coef.confidence_interval.lower_bound[i] - coef.coefficients[i]):
            sig_lags.append(i)
    return sig_lags
