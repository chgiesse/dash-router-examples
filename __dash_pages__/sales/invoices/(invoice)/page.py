import dash_mantine_components as dmc
from dash import html

from helpers import get_icon
from ._components.figures import create_comp_chart
from ._components.tabs import InvoiceTabs


def layout(children=None, invoice_id: int = None, **kwargs):
    if not invoice_id:
        return dmc.Stack(
            [
                get_icon("line-md:file-document-plus", height=60),
                dmc.Title("No invoice selected", order=3),
            ],
            align="center",
        )

    return dmc.Stack(
        [
            dmc.Title("Invoice ID: " + str(invoice_id), order=2),
            dmc.Card(
                [
                    dmc.Title("All sales of vendor", order=3, mb="md"),
                    create_comp_chart(),
                ]
            ),
            InvoiceTabs(kwargs.get('active'), invoice_id),
            dmc.Card(children),
        ]
    )
