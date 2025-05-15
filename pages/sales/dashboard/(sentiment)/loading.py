from .components import TotalSentimentGraph
from ..components.graph_card import create_graph_card_wrapper
from ..components.menu import GraphMenu

import dash_mantine_components as dmc
from dash_router import RootContainer
from dash import dcc

layout = create_graph_card_wrapper(
    graph=dmc.Center(dmc.Loader(type="oval"), h=500),
    title=TotalSentimentGraph.title, 
    menu=GraphMenu(
        graph_id=TotalSentimentGraph.ids.graph,
    ),
)
