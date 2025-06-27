import dash_mantine_components as dmc
from dash import html

from ._components.tabs import SalesTabs


def layout(children=None, **kwargs):
    tab = kwargs.get('active', 'overview')
    return dmc.Stack(
        m=0,
        p=0,
        children=[
            dmc.Title("Sales", mt=0, pt=0),
            SalesTabs(tab),
            dmc.Divider(),
            dmc.ScrollArea(
                children, h="calc(83vh)", type="auto", offsetScrollbars=True
            ),
        ],
    )
