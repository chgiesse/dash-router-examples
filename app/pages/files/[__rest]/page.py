from .components import create_route_bar

import dash_mantine_components as dmc
from typing import List


async def layout(rest: List = [], **kwargs):
    return dmc.Box(create_route_bar(rest))
