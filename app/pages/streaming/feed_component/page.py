import dash_mantine_components as dmc
from .components import FeedComponent, UserModal

async def layout(**kwargs):
    return dmc.Grid(
        [
            # dmc.GridCol(span=12),
            # dmc.GridCol(span=4),
            dmc.GridCol(
                span=12,
                children=[
                    UserModal(),
                    dmc.ScrollArea(
                        FeedComponent(),
                        mt="md",
                        h="70vh",
                        scrollbars="y",
                    ),
                ],
                # h="50vh"
            ),
        ],
    )
