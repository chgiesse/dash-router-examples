import dash_mantine_components as dmc
from dash import html
from dash_snap_grid import Grid

from .components import SlotWrapper, Tabs


def layout(
    children=None,
    slot_1=None,
    slot_2=None,
    *args,
    **kwargs,
):
    return dmc.Stack(
        [
            Tabs(),
            dmc.Flex(
                [
                    dmc.Box(
                        SlotWrapper([slot_1, slot_2], className="slots-container"),
                        # style={
                        #     "flexGrow": 1,
                        #     "flexShrink": 1,
                        #     "flexBasis": "auto",
                        #     "minWidth": 0,
                        # },
                    ),
                    dmc.Box(children, w="fit-content", mt="md"),
                ],
                style={"display": "flex", "width": "100%", "gap": "16px"},
                direction={"base": "column", "lg": "row"},
            ),
        ],
        align="center",
        # gap=0,
        justify="space-between",
    )
