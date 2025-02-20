import dash_mantine_components as dmc

from time import sleep
from .._components.cards import card
from .._components.figures import create_water_chart


def layout(**kwargs):
    invoice_id = kwargs.get("invoice_id")
    sleep(1.3)
    if invoice_id == str(1):
        1 / 0
    return dmc.Stack(
        [
            dmc.Title(f"All items for invoice id: {invoice_id}", order=3),
            create_water_chart(),
            dmc.Group([card, card], grow=True),
        ]
    )
