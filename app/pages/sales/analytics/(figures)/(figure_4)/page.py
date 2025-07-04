import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
from dash import dcc
from utils.helpers import create_theme_callback

# create_theme_callback("fig4")


async def layout(data: DataFrame, *args, **kwargs):
    theme = kwargs.get("theme")
    template = "plotly_dark" if theme else "plotly"
    labels, values = data

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.6)])
    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title=None,
        template=template,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    return dcc.Graph(figure=fig, responsive=True, id="fig4")
