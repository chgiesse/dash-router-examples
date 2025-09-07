from global_components.notifications import NotificationsContainer
from global_components.theme import ThemeComponent, theme_type
from global_components.location import Url
from utils.helpers import parse_qs, get_theme_template
from utils.constants import common_figure_config
from dash_router import RootContainer

from .api import endpoint
from plotly.subplots import make_subplots
import dash_mantine_components as dmc
from flash import callback, Input, Output, State
import plotly.graph_objects as go
from dash import dcc
import pandas as pd


class TotalSentimentGraph(dmc.Box):
    """Total Sentiment Graph implemented with Dash Mantine Components."""

    title = "Sentiment and Rating over Time"

    class ids:
        graph = "amazon-total-sentiment-graph"
        relative_switch = "amazon-total-sentiment-rel-switch"

    @callback(
        Output(ids.graph, "data"),
        Input(ids.relative_switch, "checked"),
        State(RootContainer.ids.location, "search"),
        State(ThemeComponent.ids.store, "data"),
        prevent_initial_call=True,
    )
    async def update(is_relative: bool, qs: str, is_darkmode: bool):
        try:
            query_params = parse_qs(qs)
            data = await endpoint(**query_params)

        except Exception as e:
            NotificationsContainer.send_notification(
                title="Data fetching error",
                message=str(e),
                color="red",
            )
            return

        sentiment_data = data.sentiment_data

        if is_relative:
            sentiment_data = (
                sentiment_data.divide(sentiment_data.sum(axis=1), axis=0)
                .fillna(0)
                .round(3)
            )

        # Prepare data for Mantine CompositeChart
        chart_data = TotalSentimentGraph.prepare_chart_data(
            sentiment_data, data.rating_data
        )
        return chart_data

    @staticmethod
    def prepare_chart_data(sentiment_data: pd.DataFrame, rating_data: pd.DataFrame):
        """Convert pandas DataFrames to format expected by Mantine CompositeChart."""
        # Merge sentiment and rating data
        merged_data = sentiment_data.copy()
        merged_data["AvgRating"] = rating_data["AvgRating"]

        # Reset the index to get it as a column (this will be our x-axis)
        chart_data = (
            merged_data.fillna(0).reset_index(names="dataKey").to_dict(orient="records")
        )
        return chart_data

    @staticmethod
    def figure(
        sentiment_data: pd.DataFrame,
        rating_data: pd.DataFrame,
        is_darkmode: bool = False,
    ):
        """Create a Mantine CompositeChart configuration."""
        # Define series for the sentiment values (as bars)
        sentiment_columns = sentiment_data.columns.tolist()
        series = []

        # Define colors for sentiment bars
        colors = ["violet.6", "blue.6", "teal.6", "cyan.6", "indigo.6", "green.6"]

        # Add sentiment series as bars
        for i, sentiment in enumerate(sentiment_columns):
            series.append(
                {"name": sentiment, "color": colors[i % len(colors)], "type": "bar"}
            )

        # Add rating series as a line with right y-axis
        series.append(
            {
                "name": "Average Rating",
                "color": "red.8",
                "type": "line",
                "yAxisId": "right",
            }
        )

        # Convert dataframes to format expected by Mantine CompositeChart
        merged_data = sentiment_data.copy()
        merged_data["Average Rating"] = rating_data["AvgRating"]
        chart_data = merged_data.reset_index(names="dataKey").to_dict(orient="records")

        # Create Mantine CompositeChart configuration
        chart_config = {
            "data": chart_data,
            "dataKey": "dataKey",
            "series": series,
            "barProps": {
                "isAnimationActive": True,
                "animationDuration": 800,
                "animationEasing": "ease-in-out",
                # "animationBegin": 600,
                "type": "stacked",
            },
            "lineProps": {
                "isAnimationActive": True,
                "animationDuration": 1200,
                "animationEasing": "ease-out",
                # "animationBegin": 600,
                "stroke-width": 3,
                "dot": True,
            },
            "withLegend": True,
            "legendProps": {"verticalAlign": "bottom", "height": 50},
            "gridAxis": "none",
            "tickLine": "none",
            "withXAxis": True,
            "withYAxis": True,
            "withRightYAxis": True,
            "yAxisLabel": "Sentiment classification",
            "rightYAxisLabel": "Average Rating",
            "rightYAxisProps": {"domain": [1, 5]},
            "withPointLabels": False,
            "withDots": True,
            "withTooltip": True,
            # "highlightHover": True,
        }

        return chart_config

    def __init__(
        self, sentiment_data: pd.DataFrame, rating_data: pd.DataFrame, is_darkmode: bool
    ):
        """Initialize the TotalSentimentGraph component."""
        chart_config = self.figure(sentiment_data, rating_data, is_darkmode)

        # Create Mantine CompositeChart
        composite_chart = dmc.CompositeChart(
            id=self.ids.graph,
            h=500,  # Taller height for the composite chart
            **chart_config
        )

        # Initialize parent (html.Div) with the composite chart
        super().__init__(
            children=[composite_chart],
            id=self.ids.graph,
            # className="fade-in-chart",
            # className="fade-in-right"
        )
