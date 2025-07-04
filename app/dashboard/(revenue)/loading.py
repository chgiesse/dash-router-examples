from utils.helpers import get_icon
from .components import TotalSalesGraph
from ..components.graph_card import create_graph_card_wrapper
from ..components.select import create_sale_type_select
import dash_mantine_components as dmc


layout = create_graph_card_wrapper(
    graph=dmc.Center(dmc.Loader(type="oval"), h=500),
    title=TotalSalesGraph.title,
    menu=dmc.Group(
        [
            create_sale_type_select(),
            dmc.ActionIcon(
                children=get_icon("charm:menu-kebab"),
                variant="transparent",
                # disabled=True,
                size="lg",
            ),
        ],
    ),
)
