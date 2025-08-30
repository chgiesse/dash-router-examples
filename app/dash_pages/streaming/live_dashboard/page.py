from .components import SSEGraph, MantineSSEGraph
import dash_mantine_components as dmc


def layout(*args, **kwargs):
    theme = kwargs.get("theme")
    template = "plotly_dark" if theme else "plotly"

    return [
        dmc.Button("Start stream", id="start-stream-button", mb="md"),
        dmc.SimpleGrid(
            w="100%",
            cols=1,
            children=[
                SSEGraph("Google", template),
                # SSEGraph('Amazon', template),
                # SSEGraph('Apple', template),
                # SSEGraph('TSMC', template),
                # MantineSSEGraph('Google'),
                # MantineSSEGraph('Amazon'),
                # MantineSSEGraph('Apple'),
                # MantineSSEGraph('TSMC'),
            ],
        ),
    ]
