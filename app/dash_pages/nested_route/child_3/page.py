import dash_mantine_components as dmc
from dash import html
from .models import QueryParams
from .components import ActionBar


def layout(
    slot_31=None,
    slot_32=None,
    slot_33=None,
    slot_34=None,
    slot_35=None,
    *args,
    **kwargs,
):
    params = QueryParams(**kwargs)
    return dmc.Stack(
        gap="0.25rem",
        miw="45vw",
        children=[
            ActionBar(params),
            dmc.Group([slot_31, slot_32], grow=True),
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
