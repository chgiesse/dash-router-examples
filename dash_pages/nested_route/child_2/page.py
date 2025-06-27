import dash_ag_grid as dag
import dash_mantine_components as dmc
import pandas as pd
from dash import Input, Output, callback

from .components import GridTable


def layout(*args, **kwargs):
    return dmc.Box(
        [dmc.Title("Child 2", order=2), GridTable()],
        miw="45vw",
    )
