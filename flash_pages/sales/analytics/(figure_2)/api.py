import plotly.express as px
from aiocache import cached
import asyncio 

@cached(ttl=30)
async def endpoint(*args, **kwargs):
    await asyncio.sleep(.4)
    df = px.data.carshare()
    return df
