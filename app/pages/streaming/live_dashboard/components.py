from utils.helpers import create_theme_callback, get_icon
from global_components.notifications import NotificationsContainer
from flash_router import RootContainer

import asyncio
import random
import time
from datetime import datetime

import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from dash import dcc, html
from flash import (
    ALL,
    Input,
    event_callback,
    stream_props,
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
        )

class SSEGraph(dcc.Graph):
    class ids:
        graph = lambda idx: {"type": "sse-graph-example", "index": idx}

    @event_callback(
        Input(StreamButtons.ids.start_btn, "n_clicks"),
        cancel=[
            (Input(RootContainer.ids.location, "pathname"), "/streaming/live-dashboard"),
            (Input(StreamButtons.ids.end_btn, "n_clicks", allow_optional=True), 0),
        ],
        reset_props=[
            (StreamButtons.ids.start_btn, {"disabled": False, "children": "Start stream"}),
            (StreamButtons.ids.end_btn, {"display": "none"}),
        ],
        on_error=lambda e: NotificationsContainer.send_notification(
            title="Error", message=str(e), color="red"
        )
    )
    async def update_graph(n_clicks):

        yield NotificationsContainer.send_notification(
            title="Starting stream!",
            message="Notifications in Dash, Awesome!",
            color="lime",
        )

        yield stream_props([
            (StreamButtons.ids.start_btn, {"disabled": True, "children": "Running"}),
            (StreamButtons.ids.end_btn, {"display": "flex"}),
        ])

        while True:
            await asyncio.sleep(1)
            stock_ticks = ["google", "apple", "microsoft", "amazon"]
            stocks = await asyncio.gather(*[get_stocks() for _ in stock_ticks])
            update = []
            for tick, value in zip(stock_ticks, stocks):
                update.append((SSEGraph.ids.graph(tick), {"extendData": value}))

            yield stream_props(update)

    def __init__(self, chart_type: str, template: str):
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
            title=dict(text=chart_type.title()),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )

        super().__init__(
            id=self.ids.graph(chart_type),
            figure=fig,
            style={"height": 400}
        )

create_theme_callback(SSEGraph.ids.graph(ALL))
