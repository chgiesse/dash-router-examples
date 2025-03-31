import plotly.express as px
from pandas import DataFrame
from dash import dcc
from helpers import create_theme_callback


create_theme_callback('fig3')

async def layout(data: DataFrame, *args, **kwargs):
    theme = kwargs.get('theme')
    template="mantine_dark" if theme else 'mantine_light'
    fig = px.histogram(data, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=data.columns)
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

    fig.update_layout(hovermode="x unified")
    
    return dcc.Graph(
        figure=fig,
        responsive=True,
        id='fig3'
    )