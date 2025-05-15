import dash_mantine_components as dmc
from dash_router import SlotContainer

from .components import ActionSideBar


async def layout(figures: SlotContainer, **kwargs):

    return dmc.Grid(
        children=[
            dmc.GridCol(span=9, children=figures),
            dmc.GridCol(
                ActionSideBar(),
                span=3,
                style={
                    "position": "sticky",
                    "top": 0,
                    "height": "calc(100vh - var(--mantine-spacing-xl))",
                },
            ),
        ]
    )
