import dash_mantine_components as dmc
from dash_router import ChildContainer, SlotContainer

from global_components.tabs import PageTabs
from .components import SlotWrapper


async def layout(
    children: ChildContainer,
    slot_1: SlotContainer,
    slot_2: SlotContainer,
    *args,
    **kwargs,
):
    tabs = [
        {"label": "Nested Tab 1", "href": "/nested-route/child-1"},
        {"label": "Nested Tab 2", "href": "/nested-route/child-2"},
        {"label": "Nested Tab 3", "href": "/nested-route/child-3"},
    ]

    return [
        PageTabs(tabs, children.props.active),
        dmc.Stack(
            [
                dmc.Flex(
                    [
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
                    direction={"base": "column", "lg": "row"}, # type: ignore
                ),
            ],
            align="center",
            justify="space-between",
            px="xl",
            py="md",
            style={
                "maxHeight": "calc(100dvh - var(--app-shell-footer-height) - 40px)",
                "overflowY": "auto",
                "overflowX": "hidden",
                "paddingLeft": "var(--mantine-spacing-xs)",
                "paddingRight": "var(--mantine-spacing-xs)"
            }
        )
    ]
