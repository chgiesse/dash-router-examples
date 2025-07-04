import asyncio
import random
import time
from datetime import datetime

import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from dash import dcc
from dash_extensions import SSE
from dash_extensions.streaming import sse_options
from flash import (
    ALL,
    MATCH,
    Input,
    Output,
    Patch,
    State,
    callback,
    clientside_callback,
    html,
)

from global_components.notifications import NotificationsContainer
from streaming.stream import flash_props, sse_callback

from ..models import SSEContent
from .sse_endpoint import mantine_endpoint_url


class SSEGraph(html.Div):
    class ids:
        sse = lambda idx: {"type": "test-sse", "index": idx}
        graph = lambda idx: {"type": "sse-graph", "index": idx}

    @callback(
        Output(ids.graph(ALL), "figure"),
        Input("color-scheme-toggle", "checked"),
        State(ids.graph(ALL), "id"),
        prevent_initial_call=True,
    )
    def update_figure(theme, ids):
        # template must be template object rather than just the template string name
        template = (
            pio.templates["plotly"] if not theme else pio.templates["plotly_dark"]
        )
        patched_figures = []
        for _ in ids:
            patched_fig = Patch()
            patched_fig["layout"]["template"] = template
            patched_figures.append(patched_fig)

        return patched_figures

    @sse_callback(
        Output(ids.graph(MATCH), "id"),
        Input("start-stream-button", "n_clicks"),
        Input(ids.graph(MATCH), "id"),
    )
    async def update_graph(n_clicks, component_id):
        start_time = time.time()
        multiplicator = 1
        rounds = 0

        yield await NotificationsContainer.push_notification(
            title="Starting stream!",
            action="show",
            message=component_id["index"],
            color="lime",
        )

        yield await flash_props(
            "start-stream-button", {"disabled": True, "children": "Running"}
        )

        while True:
            await asyncio.sleep(0.5)
            elapsed_time = time.time() - start_time
            y1 = random.random() * multiplicator
            y2 = random.random() * multiplicator

            if int(elapsed_time) % 10 == 0:
                multiplicator = random.randint(-1, 1) * rounds + 1
                rounds += 1

            x = datetime.now()
            update = [dict(x=[[x], [x]], y=[[y1], [y2]]), [0, 1], 100]

            yield await flash_props(component_id, {"extendData": update})

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
            title=dict(text=chart_type),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )

        super().__init__(
            children=[
                # SSE(
                #     id=self.ids.sse(chart_type),
                #     url=endpoint_url,
                #     options=sse_options(SSEContent(content='please send data')),
                #     concat=False,
                # ),
                dcc.Graph(
                    id=self.ids.graph(chart_type), figure=fig, style={"height": 450}
                )
            ]
        )


class MantineSSEGraph(html.Div):
    class ids:
        sse = lambda idx: {"type": "mantine-sse", "index": idx}
        graph = lambda idx: {"type": "mantine-graph", "index": idx}

    clientside_callback(
        """
        //js
        function ( message, data ) {
            if (!message) return window.dash_clientside.no_update;
            
            const MAX_POINTS = 50;
            const newData = JSON.parse(message);
            data.push(newData);
            data = data.slice(-MAX_POINTS)
            return data
        }   
        ;//
        """,
        Output(ids.graph(MATCH), "data"),
        Input(ids.sse(MATCH), "value"),
        State(ids.graph(MATCH), "data"),
    )

    def __init__(self, title: str):
        super().__init__(
            children=[
                SSE(
                    id=self.ids.sse(title),
                    url=mantine_endpoint_url,
                    options=sse_options(SSEContent(content="please send data")),
                    concat=False,
                ),
                dmc.Text(title, size="xl", fw=700),
                dmc.LineChart(
                    id=self.ids.graph(title),
                    h=300,
                    dataKey="date",
                    data=[],
                    series=[
                        {"name": "Apples", "color": "indigo.6"},
                        {"name": "Oranges", "color": "blue.6"},
                        {"name": "Tomatoes", "color": "teal.6"},
                    ],
                    curveType="linear",
                    tickLine="x",
                    withXAxis=True,
                    withDots=False,
                    # lineProps={
                    #     "isAnimationActive": True,
                    #     "animationDuration": 500,
                    #     "animationEasing": "ease-in-out",
                    # },
                ),
            ]
        )
