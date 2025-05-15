from global_components.notifications import NotificationsContainer
from global_components.theme import ThemeComponent, theme_type
from global_components.location import Url
from utils.helpers import parse_qs, get_theme_template
from utils.constants import common_figure_config
from dash_router import RootContainer

from .api import endpoint
from plotly.subplots import make_subplots
from flash import callback, Input, Output, State
import plotly.graph_objects as go
from dash import dcc
import pandas as pd


class TotalSentimentGraph(dcc.Graph):

    title = "Sentiment and Rating over Time"

    class ids:
        graph = "amazon-total-sentiment-graph"
        relative_switch = "amazon-total-sentiment-rel-switch"

    @callback(
        Output(ids.graph, "figure"),
        Input(ids.relative_switch, "checked"),
        State(RootContainer.ids.location, "search"),
        State(ThemeComponent.ids.toggle, "checked"),
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
            sentiment_data = sentiment_data.divide(
                sentiment_data.sum(axis=1), axis=0
            ).round(3)

        fig = TotalSentimentGraph.figure(sentiment_data, data.rating_data, is_darkmode)
        return fig

    @staticmethod
    def figure(
        sentiment_data: pd.DataFrame,
        rating_data: pd.DataFrame,
        is_darkmode: bool = False,
    ):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        template = get_theme_template(is_darkmode)

        for sentiment in sentiment_data.columns:
            fig.add_trace(
                go.Bar(
                    x=sentiment_data.index,
                    y=sentiment_data[sentiment],
                    name=f"{sentiment}",
                    text=sentiment_data[sentiment],
                    textposition="auto",
                ),
                secondary_y=False,
            )

        fig.add_trace(
            go.Scatter(
                x=rating_data.index,
                y=rating_data.AvgRating.values,
                name="Average Rating",
                line=dict(color="red", width=3),
                mode="lines+markers",
            ),
            secondary_y=True,
        )

        fig.update_layout(barmode="stack", template=template, **common_figure_config)

        fig.update_yaxes(title_text="Sentiment classification", secondary_y=False)
        fig.update_yaxes(
            title_text="Average Rating",
            secondary_y=True,
            range=[1, 5],
        )
        return fig

    def __init__(
        self, sentiment_data: pd.DataFrame, rating_data: pd.DataFrame, is_darkmode: bool
    ):
        fig = self.figure(sentiment_data, rating_data, is_darkmode)

        super().__init__(
            figure=fig,
            id=self.ids.graph,
            config={"displayModeBar": False},
        )
