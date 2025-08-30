from .components import create_route_bar, create_route_cards

import dash_mantine_components as dmc
from typing import List


async def layout(rest: List = [], **kwargs):
    return dmc.Stack([
        create_route_bar(rest),
        create_route_cards(rest)
    ])
