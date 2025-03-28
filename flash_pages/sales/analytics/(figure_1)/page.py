from pandas import DataFrame
import plotly.express as px
from dash import dcc
from helpers import create_theme_callback


create_theme_callback('fig1')

async def layout(data: DataFrame = None, *args, **kwargs):
    fig = px.box(
        data, 
        x="day", 
        y="total_bill", 
        color="smoker",
        notched=True
    )
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
        ),
    )
    return dcc.Graph(
        figure=fig.to_plotly_json(),
        responsive=True,
        animate=True,
        id='fig1'
    )
