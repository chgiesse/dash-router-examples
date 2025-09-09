from .components import SSEGraph, StreamButtons

import dash_mantine_components as dmc
from dash import dcc


async def layout(*args, **kwargs):
    theme = kwargs.get("theme")
    template = "plotly_dark" if theme else "plotly"

    return [
        StreamButtons(),
        dmc.SimpleGrid(
            w="80%",
            cols=2,
            id="graphs-grid",
            children=[
                dcc.Markdown(id="graphs-box"),
                SSEGraph("google", template),
                SSEGraph("amazon", template),
                SSEGraph("microsoft", template),
                SSEGraph("apple", template),
            ],
        ),
    ]
