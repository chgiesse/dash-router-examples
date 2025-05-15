from dash_router import SlotContainer
from dash import html
import dash_mantine_components as dmc


async def layout(
    figure_1: SlotContainer,
    figure_2: SlotContainer,
    figure_3: SlotContainer,
    figure_4: SlotContainer,
    figure_5: SlotContainer,
    **kwargs
):
    basic_container = lambda children: dmc.Box(children, h=450, p="md")

    return html.Div(
        children=[
            dmc.SimpleGrid(
                cols=2,
                children=[
                    basic_container(figure_1),
                    basic_container(figure_3),
                    basic_container(figure_5),
                    basic_container(figure_4),
                ],
            ),
            figure_2,
        ]
    )
