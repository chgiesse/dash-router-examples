from global_components.notifications import NotificationsContainer
from global_components.theme import ThemeComponent, theme_type
from global_components.location import Url
from utils.helpers import parse_qs, get_theme_template
from utils.constants import common_figure_config

from .api import endpoint
from ..models import AmazonQueryParams, SalesCallbackParams
from ..components.graph_card import create_graph_card_wrapper
from ..components.menu import GraphMenu
from ..components.switch import create_agg_switch

from dash_router import RootContainer
from pydantic import ValidationError
from flash import callback, Input, Output, State, no_update
import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px
from dash import dcc
import pandas as pd


def create_total_sales_card(data: pd.DataFrame, category: str):

    create_card = lambda title, amount: dmc.Card(
        children=[dmc.Text(title, fw=700, size="xl"), dmc.Text(amount)]
    )

    return dmc.Group(
        grow=True,
        children=[
            create_card("Category", category),
            create_card("Total Items", data.ProductCount),
            create_card("Total Amount", data.TotalPrice),
            create_card("Avg Discount", data.AvgDiscount),
        ],
    )


class CategoryRankGraph(dmc.Box):

    title = "Top Categories"

    class ids:
        graph = "amazon-top-category-graphs"
        relative_switch = "amazon-top-category-rel-switch"
        variant_select = "amazon-top-category-var-select"

    # GraphMenu.download_callback(ids.graph)
    # ThemeComponent.graph_theme_callback(ids.graph)

    @callback(
        Output(ids.graph, "figure"),
        Input(ids.relative_switch, "checked"),
        Input(ids.variant_select, "value"),
        State(ThemeComponent.ids.toggle, "checked"),
        State(RootContainer.ids.location, "search"),
        prevent_initial_call=True,
    )
    async def update(is_relative: bool, variant: str, is_darkmode: bool, qs: str):
        try:
            query_params = parse_qs(qs)
            filters = AmazonQueryParams(**query_params)
            sales_params = SalesCallbackParams(variant=variant, is_relative=is_relative)

        except ValidationError as e:
            NotificationsContainer.send_notification(
                title="Validation Error",
                message=str(e),
                color="red",
            )
            return no_update

        data = await endpoint(filters=filters, variant=sales_params.variant)

        if is_relative:
            data.ProductCount = data.ProductCount / data.ProductCount.sum()

        fig = CategoryRankGraph.figure(
            data, is_relative=is_relative, is_darkmode=is_darkmode
        )

        return fig

    @staticmethod
    def figure(
        data: pd.DataFrame, is_relative: bool = False, is_darkmode: bool = False
    ):
        template = get_theme_template(is_darkmode)

        if is_relative:
            common_props = dict(
                values=data.ProductCount,
                labels=data.MainCategory,
                hole=0.6,
                textfont=dict(size=10),
            )

            fig1 = go.Pie(**common_props, textinfo="percent", textposition="inside")

            fig2 = go.Pie(
                **common_props,
                textinfo="label",
                textposition="outside",
            )
            fig = go.Figure([fig2, fig1])
            fig.update_layout(
                margin=dict(l=100, r=80, t=40, b=40),
            )

        else:
            fig = px.bar(
                data,
                x="ProductCount",
                y="MainCategory",
                orientation="h",
                color="MainCategory",
                text_auto=True,
            )

            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

        fig.update_layout(**common_figure_config, showlegend=False, template=template)
        return fig

    def __init__(self, data: pd.DataFrame, is_darkmode: bool):
        fig = self.figure(data, is_darkmode=is_darkmode)

        super().__init__(
            create_graph_card_wrapper(
                graph=dcc.Graph(
                    figure=fig, config={"displayModeBar": False}, id=self.ids.graph
                ),
                title=self.title,
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
                            id=self.ids.variant_select,
                            value=SalesCallbackParams.get_default_variant(),
                            clearable=False,
                            allowDeselect=False,
                        ),
                        GraphMenu(
                            graph_id=self.ids.graph,
                            aggregation_items=[
                                create_agg_switch(self.ids.relative_switch)
                            ],
                        ),
                    ]
                ),
            ),
        )
