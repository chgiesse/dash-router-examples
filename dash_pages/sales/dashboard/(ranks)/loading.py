from utils.helpers import get_icon
from .components import CategoryRankGraph, create_loading_cards
from ..models import AmazonQueryParams
from ..components.graph_card import create_graph_card_wrapper
from ..components.select import create_sale_type_select
import dash_mantine_components as dmc


def layout(**kwargs):

    filters = AmazonQueryParams(**kwargs)

    if filters.is_single_view:
        return create_loading_cards()

    return create_graph_card_wrapper(
        graph=dmc.Center(dmc.Loader(type="oval"), h=500),
        title=CategoryRankGraph.title,
        menu=dmc.Group(
            [
                create_sale_type_select(),
                dmc.ActionIcon(
                    children=get_icon("charm:menu-kebab"),
                    variant="transparent",
                    # disabled=True,
                    size="lg",
                ),
            ]
        ),
    )
