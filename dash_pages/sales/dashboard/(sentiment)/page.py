from .components import TotalSentimentGraph
from ..components.graph_card import create_graph_card_wrapper
from ..components.menu import GraphMenu
from ..components.switch import create_agg_switch
from .api import SentimentEndpointResult


def layout(data: SentimentEndpointResult, **kwargs):
    is_darkmode = bool(kwargs.pop("theme", True))
    return create_graph_card_wrapper(
        graph=TotalSentimentGraph(data.sentiment_data, data.rating_data, is_darkmode),
        title=TotalSentimentGraph.title,
        menu=GraphMenu(
            graph_id=TotalSentimentGraph.ids.graph,
            aggregation_items=[
                create_agg_switch(TotalSentimentGraph.ids.relative_switch)
            ],
        ),
    )
