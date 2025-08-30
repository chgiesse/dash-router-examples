from global_components.notifications import NotificationsContainer
from utils.helpers import parse_qs

from .api import endpoint
from ..models import AmazonQueryParams, SalesCallbackParams
from ..components.graph_card import create_graph_card_wrapper
from ..components.menu import GraphMenu
from ..components.switch import create_agg_switch
from ..components.select import create_sale_type_select

from dash_router import RootContainer
from pydantic import ValidationError
from flash import callback, Input, Output, State, no_update
from dash import html
import dash_mantine_components as dmc
import pandas as pd


def create_total_sales_card(data: pd.DataFrame, category: str):

    create_card = lambda title, amount: dmc.Paper(
        children=dmc.Stack(
            [dmc.Text(title, fw=700, size="xl", className="fade-in-chart"), dmc.Text(amount, className="fade-in-chart")], gap="md"
        ),
        withBorder=True,
        h=100,
        p="xs",
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


def create_loading_cards():
    create_lc = lambda w: dmc.Paper(
        children=dmc.Stack(
            [
                dmc.Skeleton(h=18, w=w + 70, my='xs'),
                dmc.Skeleton(h=12, w=w + 70 - w * 0.5),
            ],
            gap="lg",
        ),
        withBorder=True,
        h=100,
        p="xs",
    )
    return dmc.Group(
        grow=True,
        # className="fade-in-bottom",
        children=[
            create_lc(110),
            create_lc(120),
            create_lc(115),
            create_lc(120),
        ],
    )


class CategoryRankGraph(dmc.Box):
    title = "Top Categories"

    class ids:
        graph_container = "amazon-top-category-graph-container"
        relative_switch = "amazon-top-category-rel-switch"
        variant_select = "amazon-top-category-var-select"

    @callback(
        Output(ids.graph_container, "children"),
        [
            Input(ids.relative_switch, "checked"),
            Input(ids.variant_select, "value"),
        ],
        [
            State(RootContainer.ids.location, "search"),
        ],
        prevent_initial_call=True,
    )
    async def update(is_relative: bool, variant: str, qs: str):
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

        # Apply relative calculation if needed
        if is_relative:
            data.ProductCount = (data.ProductCount / data.ProductCount.sum()).round(2)

        # Create figure based on is_relative
        return CategoryRankGraph.figure(data, is_relative)

    @staticmethod
    def figure(data: pd.DataFrame, is_relative: bool = False):
        colors = ["cyan.6", "violet.6", "blue.6", "teal.6"]
        if is_relative:
            return dmc.Center(
                dmc.DonutChart(
                    data=[
                        {
                            "name": row["MainCategory"],
                            "value": row["ProductCount"],
                            "color": colors[i],
                        }
                        for i, (_, row) in enumerate(data.iterrows())
                    ],
                    withLabels=False,
                    withLabelsLine=False,
                    withTooltip=True,
                    size=200,
                    strokeWidth=1.8,
                    className="fade-in-chart",
                    pieProps={
                        "isAnimationActive": True,
                        "animationDuration": 500,
                        "animationEasing": "ease-in-out",
                        # "animationBegin": 50,
                    },
                    thickness=25,
                ),
                h=500,
            )
        else:
            return dmc.BarChart(
                h=500,
                data=[
                    {
                        "category": row["MainCategory"],
                        "count": row["ProductCount"],
                    }
                    for _, row in data.iterrows()
                ],
                dataKey="category",
                orientation="vertical",
                series=[{"name": "count", "color": "blue.6"}],
                withLegend=False,
                withTooltip=True,
                yAxisProps={"width": 160},
                # className="fade-in-chart",
                className='fade-in-left',
                barProps={
                    "isAnimationActive": True,
                    "animationDuration": 500,
                    "animationEasing": "ease-in-out",
                },

            )

    def __init__(self, data: pd.DataFrame):
        initial_chart = self.figure(data, is_relative=False)

        super().__init__(
            children=create_graph_card_wrapper(
                graph=html.Div(
                    children=initial_chart,
                    id=self.ids.graph_container,
                ),
                title=self.title,
                menu=dmc.Group(
                    [
                        create_sale_type_select(self.ids.variant_select),
                        GraphMenu(
                            graph_id=self.ids.graph_container,
                            aggregation_items=[
                                create_agg_switch(self.ids.relative_switch)
                            ],
                        ),
                    ]
                ),
            ),
        )
