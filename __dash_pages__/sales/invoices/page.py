import dash_mantine_components as dmc
from dash import html

from ._components.figures import bar_chart


def layout(invoice=None, overview=None, **kwargs):
    return dmc.SimpleGrid(
        cols=2,
        children=[
            dmc.Stack(
                [
                    dmc.Card(dmc.Stack([dmc.Title("Top Vendors", order=2), bar_chart])),
                    dmc.Card(dmc.Stack([dmc.Title("Invoice list", order=3), overview])),
                ],
                gap="lg",
            ),
            dmc.Stack(
                [
                    dmc.Box(invoice, mih=50),
                    dmc.Alert(
                        "This is still the invoices section",
                        title="Invoices section!",
                    ),
                ]
            ),
        ],
    )
