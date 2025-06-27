from time import sleep
import plotly.express as px 


def endpoint(*args, **kwargs):
    sleep(0.2)
    df = px.data.tips()
    return df
