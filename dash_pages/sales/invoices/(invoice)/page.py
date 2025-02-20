import dash_mantine_components as dmc
from dash_router import RouteConfig, ChildContainer

from time import sleep
from helpers import get_icon
from ._components.figures import create_comp_chart
from ._components.tabs import InvoiceTabs

config = RouteConfig(path_template="<invoice_id>", default_child="items")


def layout(children: ChildContainer, invoice_id: int = None, **kwargs):
    if not invoice_id:
        return dmc.Stack(
            [
                get_icon("carbon:select-01", height=60),
                dmc.Title("No invoice selected", order=3),
            ],
            align="center",
        )
    
    sleep(1.2)
    return dmc.Stack(
        [
            dmc.Title("Invoice ID: " + str(invoice_id), order=2),
            dmc.Card(
                [
                    dmc.Title("All sales of vendor", order=3, mb="md"),
                    create_comp_chart(),
                ]
            ),
            InvoiceTabs(children.props.active, invoice_id),
            dmc.Card(children),
        ]
    )
