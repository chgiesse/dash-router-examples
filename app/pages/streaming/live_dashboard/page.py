from .components import SSEGraph, StreamButtons
import dash_mantine_components as dmc


async def layout(*args, **kwargs):
    theme = kwargs.get("theme")
    template = "plotly_dark" if theme else "plotly"

    return [
        StreamButtons(),
        dmc.SimpleGrid(
            cols={"xxl": 2, "xl": 2, "lg": 2, "md": 1, "sm": 1, "xs": 1, "xxs": 1}, # type: ignore
            id="graphs-grid",
            children=[
                SSEGraph("google", template),
                SSEGraph("amazon", template),
                SSEGraph("microsoft", template),
                SSEGraph("apple", template),
            ],
        ),
    ]
