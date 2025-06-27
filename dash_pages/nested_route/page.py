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
            # Grid(
            #     id="grid",
            #     cols=12,
            #     rowHeight=100,
            #     layout=[
            #         # i should match the id of the children
            #         {"i": "1", "x": 0, "y": 0, "w": 1, "h": 2},
            #         {"i": "2", "x": 1, "y": 0, "w": 3, "h": 2},
            #         {"i": "3", "x": 4, "y": 0, "w": 1, "h": 2},
            #     ],
            #     children=[
            #         dmc.Box(
            #             "1", id="1", style={"background": "lightblue", "height": "100%"}
            #         ),
            #         dmc.Box(
            #             "2", id="2", style={"background": "lightgreen", "height": "100%"}
            #         ),
            #         dmc.Box(
            #             "3", id="3", style={"background": "lightcoral", "height": "100%"}
            #         ),
            #     ],
            # ),
            dmc.Flex(
                children=[
                    dmc.Box(
                        SlotWrapper([slot_1, slot_2], className="slots-container"),
                        style={
                            "flexGrow": 1,
                            "flexShrink": 1,
                            "flexBasis": "auto",
                            "minWidth": 0,
                        },
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
