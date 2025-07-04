import dash_mantine_components as dmc
from dash import html
from dash_router import RouteConfig, ChildContainer

config = RouteConfig(
    default_child="overview"
)

from ._components.tabs import SalesTabs, Tabs


def layout(children: ChildContainer, **kwargs):
    tab = children.props.active
    return dmc.Stack(
        gap="sm",
        children=[
            dmc.Paper(
                SalesTabs(tab),
                withBorder=True,
                radius="xl",
                p=5,
                w="fit-content",
                mx="auto",
                className='fade-in-top',
            ),
            children,
        ],
    )
