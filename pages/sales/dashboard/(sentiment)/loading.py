from utils.helpers import get_icon
from .components import TotalSentimentGraph
from ..components.graph_card import create_graph_card_wrapper

import dash_mantine_components as dmc

# layout = dmc.Center(dmc.Loader(type="oval"), h=500)

layout = create_graph_card_wrapper(
    graph=dmc.Center(dmc.Loader(type="oval"), h=500),
    title=TotalSentimentGraph.title,
    menu=dmc.ActionIcon(
        children=get_icon("charm:menu-kebab"),
        variant="transparent",
        # disabled=True,
        size="lg",
    ),
)
