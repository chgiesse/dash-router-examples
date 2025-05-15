from .components import CategoryRankGraph
from ..models import SalesCallbackParams
from ..components.graph_card import create_graph_card_wrapper
from ..components.menu import GraphMenu
import dash_mantine_components as dmc
from dash_router import RootContainer
from dash import dcc

layout = create_graph_card_wrapper(
    graph=dmc.Center(dmc.Loader(type="oval"), h=500),
    title=CategoryRankGraph.title,
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
                id=CategoryRankGraph.ids.variant_select,
                value=SalesCallbackParams.get_default_variant(),
                clearable=False,
                allowDeselect=False,
                disabled=True
            ),
            GraphMenu(graph_id=CategoryRankGraph.ids.graph),
        ]
    ),
)
