from .components import InvoicePagination

import dash_mantine_components as dmc
from dash_router import SlotContainer, ChildContainer
from dash import dcc


async def layout(children: ChildContainer, overview: SlotContainer, **kwargs):

    page = int(kwargs.get("page", 1))

    bar_data = [
        {"month": "Amazon", "Smartphones": 1200, "Laptops": 900, "Tablets": 200},
        {"month": "Apple", "Smartphones": 1900, "Laptops": 1200, "Tablets": 400},
        {"month": "Nvidia", "Smartphones": 400, "Laptops": 1000, "Tablets": 200},
        {"month": "AMD", "Smartphones": 1000, "Laptops": 200, "Tablets": 800},
        {"month": "Microsoft", "Smartphones": 800, "Laptops": 1400, "Tablets": 1200},
        {"month": "SAP", "Smartphones": 750, "Laptops": 600, "Tablets": 1000},
    ]

    return dmc.SimpleGrid(
        cols={"xl": 2, "lg": 2, "md": 1, "sm": 1, "xs": 1},
        children=[
            dmc.Stack(
                [
                    dmc.Title("Top Vendors", order=3),
                    dmc.Box(
                        h=300,
                        children=dmc.BarChart(
                            h=300,
                            dataKey="month",
                            data=bar_data,
                            orientation="vertical",
                            yAxisProps={"width": 80},
                            series=[{"name": "Smartphones", "color": "violet.4"}],
                            barProps={"isAnimationActive": True, "radius": 50},
                            gridAxis="none",
                        ),
                    ),
                    dmc.Title("Invoice list", order=3),
                    overview,
                    InvoicePagination(page)
                ]
            ),
            children,
            # dmc.Stack(
            #     [
            #         children,
            #         dmc.Alert(
            #             "This is still the invoices section",
            #             title="Invoices section!",
            #             mt="auto",
            #         ),
            #     ]
            # ),
        ],
    )
