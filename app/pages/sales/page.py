import dash_mantine_components as dmc
from dash_router import ChildContainer, RouteConfig

from ._components.tabs import SalesTabs, Tabs

config = RouteConfig(default_child="overview")


async def layout(children: ChildContainer = None, **kwargs):
    tab = children.props.active
    return dmc.Stack(
        children=[
            SalesTabs(tab),
            dmc.Box(
                children,
                mx={"xxl": "12.5%", "xl": "7.5%", "lg": "7.5%", "md": "7.5%", "sm": "5%", "xs": "2.5%", "xxs": "2.5%"},
                # w={"xxl": "75%", "xl": "85%", "lg": "85%", "md": "85%", "sm": "90%", "xs": "95%", "xxs": "95%"},
            ),
        ],
    )
