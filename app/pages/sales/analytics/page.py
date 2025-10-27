import dash_mantine_components as dmc
from dash_router import SlotContainer

from .components import ActionSideBar


async def layout(figures: SlotContainer, **kwargs):

    return dmc.Grid(
        [
            dmc.GridCol(
                figures,
                span={"xl": 9, "lg": 9, "md": 9, "sm": 12, "xs": 12, "xxs": 12}, # type: ignore
                order={"xl": 1, "lg": 1, "md": 1, "sm": 2, "xs": 2, "xxs": 2}, # type: ignore
            ),
            dmc.GridCol(
                ActionSideBar(),
                span={"xl": 3, "lg": 3, "md": 3, "sm": 12, "xs": 12, "xxs": 12}, # type: ignore
                order={"xl": 2, "lg": 2, "md": 2, "sm": 1, "xs": 1, "xxs": 1}, # type: ignore
            ),
        ],
    )
