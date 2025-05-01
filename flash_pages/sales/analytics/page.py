import dash_mantine_components as dmc
from dash_router import SlotContainer

from .components import ActionSideBar


async def layout(
    figure_1: SlotContainer,
    figure_2: SlotContainer,
    figure_3: SlotContainer,
    figure_4: SlotContainer,
    figure_5: SlotContainer,
    **kwargs
):

    basic_container = lambda children: dmc.Box(children, h=450, p='md')

    return dmc.Grid(
        children=[
            dmc.GridCol(
                span=9,
                children=[
                    dmc.SimpleGrid(
                        # m=0, p=0, spacing='xs',
                        cols=2,
                        children=[
                            basic_container(figure_1),
                            basic_container(figure_3),
                            basic_container(figure_5),
                            basic_container(figure_4),
                        ]
                    ),
                    figure_2,
                ]
            ),
            dmc.GridCol(
                ActionSideBar(), 
                span=3,
                style={
                    'position': 'sticky',
                    'top': 0,
                    'height': 'calc(100vh - var(--mantine-spacing-xl))'
                }
            ),
        ]
    )
