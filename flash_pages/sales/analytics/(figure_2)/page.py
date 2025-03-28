import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
from dash import dcc
from helpers import create_theme_callback


create_theme_callback('fig2')

async def layout(data: DataFrame, *args, **kwargs):
    x=['Winter', 'Spring', 'Summer', 'Fall']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=[40, 60, 40, 10],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one' # define stack group
    ))
    fig.add_trace(go.Scatter(
        x=x, y=[20, 10, 10, 60],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=[40, 30, 50, 30],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(184, 247, 212)'),
        stackgroup='one'
    ))

    fig.update_layout(yaxis_range=(0, 100))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title=None,
        template="plotly_dark",
        modebar={
            "orientation": "v",
            "bgcolor": "rgba(0,0,0,0)",
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        )
    )

    return dcc.Graph(
        figure=fig,
        responsive=True,
        animate=True,
        id='fig2'
    )