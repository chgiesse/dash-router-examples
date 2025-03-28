from .components import SSEGraph, MantineSSEGraph
import dash_mantine_components as dmc


async def layout(*args, **kwargs):
    return dmc.SimpleGrid(
        w='100%',
        cols=2,
        children=[
            SSEGraph('Google'),
            SSEGraph('Amazon'),
            SSEGraph('Apple'),
            SSEGraph('TSMC'),
            # MantineSSEGraph()
        ], 
)