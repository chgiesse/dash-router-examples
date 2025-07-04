import dash_mantine_components as dmc
from dash import html

from .components import ActionSideBar


def layout(figures=None, **kwargs):

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
