import dash_mantine_components as dmc
from dash_router import RouteConfig, ChildContainer

from ._components.tabs import SalesTabs

config = RouteConfig(default_child="overview")


def layout(children: ChildContainer = None, **kwargs):
    tab = children.props.active
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
