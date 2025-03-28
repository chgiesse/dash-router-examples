import dash_ag_grid as dag
import dash_mantine_components as dmc
import pandas as pd
from flash import Input, Output, clientside_callback

from .components import GridTable

async def layout(*args, **kwargs):
    return dmc.Box(
        [
            dmc.Title("Child 2", order=2),
            GridTable()
        ],
        miw="45vw",
    )
