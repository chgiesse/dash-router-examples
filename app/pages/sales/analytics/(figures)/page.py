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
    basic_container = lambda children, **kwargs: dmc.Card(
        children, h=450, className="fade-in-chart", p=0, **kwargs
    )

    return dmc.Box(
        [
            dmc.SimpleGrid(
                cols={
                    "xxl": 2,
                    "xl": 2,
                    "lg": 2,
                    "md": 2,
                    "sm": 1,
                    "xs": 1,
                    "xxs": 1
                }, # type: ignore
                children=[
                    basic_container(figure_1),
                    basic_container(figure_3),
                    basic_container(figure_5),
                    basic_container(figure_4),
                ],
            ),
            basic_container(figure_2, my="md"),
        ]
    )
