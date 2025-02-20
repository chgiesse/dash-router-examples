import dash_mantine_components as dmc

from router import RouteConfig
from router.components import ChildContainer

from ._components.tabs import SalesTabs

config = RouteConfig(default_child="overview")


async def layout(children: ChildContainer = None, **kwargs):
    # def layout(children: ChildContainer = None, **kwargs):
    tab = children.props.active
    print("Tab in sales: ", tab, flush=True)
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
