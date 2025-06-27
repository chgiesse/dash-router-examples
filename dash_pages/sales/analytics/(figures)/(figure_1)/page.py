from pandas import DataFrame
import plotly.express as px
from dash import dcc
from utils.helpers import create_theme_callback


create_theme_callback("fig1")


def layout(data: DataFrame = None, *args, **kwargs):
    theme = kwargs.get("theme")
    template = "plotly_dark" if theme else "plotly"
    fig = px.box(data, x="day", y="total_bill", color="smoker", notched=True)
    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        xaxis_title=None,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        template=template,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )
    return dcc.Graph(
        figure=fig,
        responsive=True,
        id="fig1",
    )
