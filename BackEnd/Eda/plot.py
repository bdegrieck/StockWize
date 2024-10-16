import pandas as pd
from plotly.subplots import make_subplots
from pydantic.v1 import BaseModel
import plotly.graph_objects as go
import statsmodels.api as sma

class MSTLGraph(BaseModel):
    """
    xaxis_data (pd.Series) data of the x-axis
    yaxis_data (pd.Series) data of the y-axis
    x_title (str): title of the x-axis
    y_ttile (str); title of the y-axis
    title (str): title of the subgraph
    """
    xaxis_data: pd.Series
    yaxis_data: pd.Series
    x_title: str
    y_title: str
    title: str

    class Config:
        arbitrary_types_allowed = True


class ACFGraph(BaseModel):
    """
    data (pd.Series): Series of data you want to plot
    title (str): title of the plot
    """
    data: pd.Series
    title: str

    class Config:
        arbitrary_types_allowed = True



class PACFGraph(BaseModel):
    """
    data (pd.Series): Series of data you want to plot
    title (str): title of the plot
    """
    data: pd.Series
    title: str

    class Config:
        arbitrary_types_allowed = True



def plot(graphs: list[MSTLGraph], main_title: str):
    """
    Function to plot n_rows sub graphs
    Args:
        graphs (MSTLGraph): Graph object that contains the data and titles
        main_title (str): title of the chart

    Returns:
        fig - Figure plot
    """

    fig = make_subplots(rows=len(graphs), cols=1, shared_xaxes=True)

    for row, graph in zip(range(1, len(graphs) + 1), graphs):
        fig.add_trace(go.Scatter(x=graph.xaxis_data, y=graph.yaxis_data, mode='lines', name=graph.title), row=row, col=1)
        fig.update_xaxes(title_text=graph.x_title, row=row, col=1)
        fig.update_yaxes(title_text=graph.y_title, row=row, col=1)

    fig.update_layout(
        title=main_title,
        height=800,
        template='plotly_white',
        showlegend=False
    )

    return fig


def plot_acf(graph: ACFGraph):
    """
    Plotting acf graphs
    Args:
        graph (ACFGraph): Acf graph object you want to plot

    Returns:
        fig - figure of the plot
    """
    fig = sma.graphics.tsa.plot_acf(x=graph.data, title=graph.title)
    return fig


def plot_pacf(graph: PACFGraph):
    """
    Plotting acf graphs
    Args:
        graph (ACFGraph): Pacf graph object you want to plot

    Returns:
        fig - figure of the plot
    """
    fig = sma.graphics.tsa.plot_pacf(x=graph.data, title=graph.title)
    return fig
