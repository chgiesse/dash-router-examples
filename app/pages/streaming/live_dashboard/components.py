from utils.helpers import create_theme_callback, get_icon
from global_components.notifications import NotificationsContainer
from global_components.theme import ThemeComponent
from flash_router import RootContainer

import asyncio
import random
import time
from datetime import datetime

import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from flash import (
    ALL,
    Input,
    event_callback,
    stream_props,
    State
)

count = 0
start_time = time.time()
multiplicator = 1

def get_count():
    global count
    count += 1
    return count

async def get_stocks():
    global start_time, multiplicator
    rounds = get_count()
    elapsed_time = time.time() - start_time
    y1 = random.random() * multiplicator
    y2 = random.random() * multiplicator

    if int(elapsed_time) % 10 == 0:
        multiplicator = random.randint(-1, 1) * rounds + 1
        rounds += 1

    x = datetime.now()
    update = [dict(x=[[x], [x]], y=[[y1], [y2]]), [0, 1], 100]
    return update


class StreamButtons(dmc.Group):
    class ids:
        start_btn = "start-stream-button"
        end_btn = "end-stream-button"

    def __init__(self):
        super().__init__(
            children=[
                dmc.Button(
                    "Start stream",
                    id=self.ids.start_btn,
                ),
                dmc.Button(
                    "End stream",
                    id=self.ids.end_btn,
                    display="none",
                    leftSection=get_icon("mingcute:stop-circle-line", height=15),
                    color="red",
                    variant="outline",
                ),
            ],
            mb="md",
            justify="flex-end",
        )

class SSEGraph(dcc.Graph):
    class ids:
        graph = lambda idx: {"type": "sse-graph-example", "index": idx}

    @event_callback(
        Input(StreamButtons.ids.start_btn, "n_clicks"),
        State(ThemeComponent.ids.store, "data"),
        on_error=lambda e: NotificationsContainer.send_notification(
            title="Error", message=str(e), color="red"
        ),
        cancel=[
            (Input(RootContainer.ids.location, "pathname"), "streaming/live-dashboard"),
            (Input(StreamButtons.ids.end_btn, "n_clicks", allow_optional=True), 0),
        ],
        reset_props=[
            (StreamButtons.ids.start_btn, {"disabled": False, "children": "Start stream"}),
            (StreamButtons.ids.end_btn, {"display": "none"}),
        ],
        prevent_initial_call=False
    )
    async def update_graph(n_clicks = None, is_dark = None):
        stock_ticks = ["google", "apple", "microsoft", "amazon"]

        yield NotificationsContainer.send_notification(
            title="Starting stream!",
            message="Notifications in Dash, Awesome!",
            color="lime",
        )

        init_figs = [
            (
                SSEGraph.ids.graph(tick),
                {
                    "figure": SSEGraph.create_figure(
                        "plotly_dark" if is_dark else "plotly",
                        tick.capitalize()
                    ),
                    "style": {"visibility": "visible"}
                }
            )
                for tick in stock_ticks
        ]

        yield stream_props([
            (StreamButtons.ids.start_btn, {"disabled": True, "children": "Running"}),
            (StreamButtons.ids.end_btn, {"display": "flex"}),
            *init_figs
        ])

        while True:
            await asyncio.sleep(1)
            stocks = await asyncio.gather(*[get_stocks() for _ in stock_ticks])
            update = []
            for tick, value in zip(stock_ticks, stocks):
                update.append((SSEGraph.ids.graph(tick), {"extendData": value}))

            yield stream_props(update)

    @staticmethod
    def create_figure(template: str, title: str):
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=pd.Series(dtype=object),
                y=pd.Series(dtype=object),
                mode="lines+markers",
                name="trace-1",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=pd.Series(dtype=object),
                y=pd.Series(dtype=object),
                mode="lines+markers",
                name="trace-2",
            )
        )
        fig.update_layout(hovermode="x unified")

        fig.update_layout(
            template=template,
            xaxis_title=None,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title=dict(text=title),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        return fig

    def __init__(self, chart_type: str, template: str):

        super().__init__(
            id=self.ids.graph(chart_type),
            style={"height": 400, "visibility": "hidden"},
            responsive=True,
        )

create_theme_callback(SSEGraph.ids.graph(ALL))
