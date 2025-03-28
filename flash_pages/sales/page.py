import dash_mantine_components as dmc
from dash_router import ChildContainer, RouteConfig

from ._components.tabs import SalesTabs, Tabs

config = RouteConfig(default_child="overview")


async def layout(children: ChildContainer = None, **kwargs):
    tab = children.props.active
    return dmc.Stack(
        gap='sm',
        children=[
            dmc.Paper(
                SalesTabs(tab), 
                withBorder=True, 
                radius='xl', 
                p=5, 
                w='fit-content',
                mx='auto'
            ),
            children
        ],
    )
