from .components import TotalSalesGraph
from ..components.graph_card import create_graph_card_wrapper
from ..components.menu import GraphMenu
from ..components.switch import create_agg_switch
from ..components.select import create_sale_type_select
from ..models import SalesCallbackParams

import dash_mantine_components as dmc
import pandas as pd


def layout(data: pd.DataFrame, **kwargs):
    graph = TotalSalesGraph(data)
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
                create_sale_type_select(graph.ids.variant_select),
                GraphMenu(
                    graph_id=graph.ids.graph,
                    aggregation_items=[
                        create_agg_switch(graph.ids.relative_switch),
                        create_agg_switch(graph.ids.running_switch, title="Running"),
                    ],
                    application_items=[
                        create_agg_switch(graph.ids.table_switch, title="Table view")
                    ],
                ),
            ]
        ),
    )
