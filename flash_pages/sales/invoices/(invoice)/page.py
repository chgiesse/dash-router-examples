import dash_mantine_components as dmc
from dash_router import RouteConfig, ChildContainer

from helpers import get_icon

config = RouteConfig(path_template="<invoice_id>", default_child="items")


async def layout(children: ChildContainer = None, data: any = None, invoice_id: int = None, **kwargs):
    if not data:
        return dmc.Stack(
            [
                get_icon("material-symbols:select-window-2-outline", height=60),
                dmc.Title("No invoice selected", order=3),
            ],
            align="center",
        )
    
    return dmc.Stack(
        justify='flex-start',
        gap='lg',
        children=[
            dmc.Title("All sales of vendor with ID " + str(invoice_id), order=3, mb="md"),
            dmc.CompositeChart(
                h=250,
                data=data,
                dataKey="date",
                withLegend=True,
                maxBarWidth=30,
                gridAxis="none",
                lineProps={
                    "isAnimationActive": True,
                    "animationDuration": 500,
                    "animationEasing": "ease-in-out",
                },
                barProps={
                    "isAnimationActive": True,
                    "animationDuration": 500,
                    "animationEasing": "ease-in-out",
                },
                areaProps={
                    "isAnimationActive": True,
                    "animationDuration": 500,
                    "animationEasing": "ease-in-out",
                },
                series=[
                    {"name": "Tomatoes", "color": "violet.3", "type": "bar"},
                    {"name": "Apples", "color": "blue.3", "type": "line"},
                    {"name": "Oranges", "color": "violet.9", "type": "area"},
                ],
            ),
            dmc.Tabs(
                value=children.props.active,
                children=dmc.TabsList(
                    [
                        dmc.Anchor(
                            dmc.TabsTab("Items", value="items"),
                            href=f"/sales/invoices/{str(invoice_id)}/items",
                            underline=False,
                        ),
                        dmc.Anchor(
                            dmc.TabsTab("Positions", value="positions"),
                            href=f"/sales/invoices/{str(invoice_id)}/positions",
                            underline=False,
                        ),
                        dmc.Anchor(
                            dmc.TabsTab("Conversation", value="conversation"),
                            href=f"/sales/invoices/{str(invoice_id)}/conversation",
                            underline=False,
                            ml="auto"
                        ),
                    ]
                )
            ),
            children
        ]
    ) 
