import dash_mantine_components as dmc
from dash_router import ChildContainer, SlotContainer
from dash_snap_grid import Grid

from .components import SlotWrapper, Tabs


async def layout(
    children: ChildContainer,
    slot_1: SlotContainer = None,
    slot_2: SlotContainer = None,
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
        justify="space-between",
        px="xl",
        py="md",
        style={
            "maxHeight": "calc(100dvh - var(--app-shell-header-height))",
            "overflowY": "auto",
            "overflowX": "hidden",
            "paddingLeft": "var(--mantine-spacing-xs)",
            "paddingRight": "var(--mantine-spacing-xs)"
        }
    )
