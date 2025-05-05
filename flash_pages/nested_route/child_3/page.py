import dash_mantine_components as dmc
from dash_router import RouteConfig, SlotContainer
from .models import QueryParams
from .components import ActionBar, ResizeGrid

config = RouteConfig(default_child="child-11")


async def layout(
    slot_31: SlotContainer = None,
    slot_32: SlotContainer = None,
    slot_33: SlotContainer = None,
    slot_34: SlotContainer = None,
    slot_35: SlotContainer = None,
    *args,
    **kwargs,
):
    params = QueryParams(**kwargs)
    return dmc.Stack(
        gap="0.25rem",
        miw='45vw',
        children=[
            ActionBar(params),
            dmc.Group(
                [slot_31, slot_32],
                grow=True
            ),
            # ResizeGrid(slot_31, slot_32),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        children=[
                            dmc.TabsTab("Slot 3", value="gallery"),
                            dmc.TabsTab("Slot 4", value="messages"),
                            dmc.TabsTab("Slot 5", value="settings"),
                        ]
                    ),
                    dmc.TabsPanel(slot_33, value="gallery", mt="md"),
                    dmc.TabsPanel(slot_34, value="messages", mt="md"),
                    dmc.TabsPanel(slot_35, value="settings", mt="md"),
                ],
                orientation="horizontal", 
                variant="default",
                value="gallery",
                mb="md",
            ),
        ],
    )   
