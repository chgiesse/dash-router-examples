from utils.helpers import create_theme_callback

import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
from dash import dcc


create_theme_callback('fig5')

async def layout(data: DataFrame = None, *args, **kwargs):
    theme = kwargs.get('theme')
    template="plotly_dark" if theme else 'plotly'
    fig = go.Figure(go.Sunburst(
        labels=data.get('labels'),
        parents=data.get('parents'),
        values=data.get('values')
    ))
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

    return dcc.Graph(
        figure=fig,
        responsive=True,
        id='fig5'
    )