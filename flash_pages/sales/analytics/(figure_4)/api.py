from aiocache import cached
import asyncio 

# @cached(ttl=30)
async def endpoint(*args, **kwargs):
    await asyncio.sleep(.6)
    labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
    values = [4500, 2500, 1053, 500]

    return labels, values
