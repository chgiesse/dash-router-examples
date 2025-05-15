from .components import TotalSalesGraph
from ..components.graph_card import create_graph_card_wrapper
from ..components.menu import GraphMenu
from ..components.switch import create_agg_switch
from ..models import SalesCallbackParams

import dash_mantine_components as dmc 
import pandas as pd

async def layout(data: pd.DataFrame, **kwargs):
    is_darkmode = bool(kwargs.pop("theme", True))
    graph = TotalSalesGraph(data, is_darkmode)
    table = graph.table(data)
    
    graph_container = dmc.Box(
        children=[
            dmc.Center(
                table,
                className=graph.ids.table,
                **{"data-hidden": True},
            ),
            dmc.Box(graph, className=graph.ids.graph, **{"data-hidden": False}),
        ],
    )

    return create_graph_card_wrapper(
        graph=graph_container,
        title=graph.title,
        menu=dmc.Group(
            [
                dmc.Select(
                    data=[
                        {"value": val, "label": val.title()}
                        for val in SalesCallbackParams.get_variants()
                    ],
                    placeholder="variant",
                    size="sm",
                    w=120,
                    id=graph.ids.variant_select,
                    value=SalesCallbackParams.get_default_variant(),
                    clearable=False,
                    allowDeselect=False,
                ),
                GraphMenu(
                    graph_id=graph.ids.graph,
                    aggregation_items=[
                        create_agg_switch(graph.ids.relative_switch),
                        create_agg_switch(
                            graph.ids.running_switch, title="Running"
                        ),
                    ],
                    application_items=[
                        create_agg_switch(
                            graph.ids.table_switch, title="Table view"
                        )
                    ],
                ),
            ]
        ),
    )

