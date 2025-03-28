import dash_mantine_components as dmc
from dash_router import ChildContainer, SlotContainer

from .components import SlotWrapper, Tabs


async def layout(
    children: ChildContainer,
    slot_1: SlotContainer = None,
    slot_2: SlotContainer = None,
    *args,
    **kwargs,
):
    return dmc.Stack([
        Tabs(),
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
                dmc.Box(
                    children,
                    w='fit-content',
                    mt='md'
                ),
            ],
            style={
                "display": "flex", 
                "width": "100%", 
                "gap": "16px"
            },
            direction={
                "base": "column", 
                "lg": "row"
            }
        )
    ], 
    align='center', 
    # gap=0, 
    justify='space-between'
)
