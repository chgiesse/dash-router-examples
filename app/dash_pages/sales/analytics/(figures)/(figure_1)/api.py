import plotly.express as px
from time import sleep


def endpoint(*args, **kwargs):
    sleep(0.8)
    df = px.data.tips()
    return df
