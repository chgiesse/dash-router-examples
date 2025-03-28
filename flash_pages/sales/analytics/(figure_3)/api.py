import plotly.express as px
from aiocache import cached
import asyncio 

@cached(ttl=30)
async def endpoint(*args, **kwargs):
    print('Execute figure 3 data', flush=True)
    await asyncio.sleep(.2)
    df = px.data.tips()
    return df
