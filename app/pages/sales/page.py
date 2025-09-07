import dash_mantine_components as dmc
from dash_router import ChildContainer, RouteConfig

from ._components.tabs import SalesTabs, Tabs

config = RouteConfig(default_child="overview")


async def layout(children: ChildContainer = None, **kwargs):
    tab = children.props.active
    return dmc.ScrollArea(
            children=[
                dmc.Paper(
                    SalesTabs(tab),
                    # withBorder=True,
                    radius="xl",
                    p=5,
                    w="fit-content",
                    mx="auto",
                    className='fade-in-top',
                ),
                children,
            ],
        h="calc(100dvh - var(--appshell-header-height))",
        type="scroll",
        px="xl",
        # p="md",
    )
