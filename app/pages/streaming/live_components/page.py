import dash_mantine_components as dmc
from .components import TestComponentStream


async def layout(*args, **kwargs):
    return dmc.Stack([dmc.Title("Stream Components"), TestComponentStream()])
