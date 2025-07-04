from time import sleep
import plotly.express as px 


def endpoint(*args, **kwargs):
    sleep(1)
    df = px.data.carshare()
    return df
