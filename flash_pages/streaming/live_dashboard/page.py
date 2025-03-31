from .components import SSEGraph, MantineSSEGraph
import dash_mantine_components as dmc


async def layout(*args, **kwargs):
    theme = kwargs.get('theme')
    template="mantine_dark" if theme else 'mantine_light'

    return dmc.SimpleGrid(
        w='100%',
        cols=2,
        children=[
            SSEGraph('Google', template),
            SSEGraph('Amazon', template),
            SSEGraph('Apple', template),
            SSEGraph('TSMC', template),
            # MantineSSEGraph()
        ], 
)