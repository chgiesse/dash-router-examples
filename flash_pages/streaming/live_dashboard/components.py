from ..models import SSEContent
from ..sse_endpoint import endpoint_url, mantine_endpoint_url
from dash_extensions import SSE
from dash_extensions.streaming import sse_options
import dash_mantine_components as dmc 
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from dash import dcc
from flash import (
    html,  
    clientside_callback,
    Input, 
    Output, 
    State,
    MATCH,
    callback,
    ALL,
    Patch
)


class SSEGraph(html.Div):
    
    class ids:
        sse = lambda idx: {'type': 'test-sse', 'index': idx}
        graph = lambda idx: {'type': 'sse-graph', 'index': idx}

    @callback(
        Output(ids.graph(ALL), "figure"),
        Input("color-scheme-toggle", "checked"),
        State(ids.graph(ALL), "id"),
        prevent_initial_call=True
    )
    def update_figure(theme, ids):
        # template must be template object rather than just the template string name
        template = pio.templates["mantine_light"] if not theme else pio.templates["mantine_dark"]
        patched_figures = []
        for _ in ids:
            patched_fig = Patch()
            patched_fig["layout"]["template"] = template
            patched_figures.append(patched_fig)

        return patched_figures
    
    clientside_callback(
        '''
        //js
        function(message, figure) {
            if (!message) return window.dash_clientside.no_update;

            const MAX_POINTS = 50;
            const data = JSON.parse(message);
            const newFigure = JSON.parse(JSON.stringify(figure));
            newFigure.data[0].x.push(data.x);
            newFigure.data[0].y.push(data.y1);

            newFigure.data[1].x.push(data.x);
            newFigure.data[1].y.push(data.y2);
            
            if (newFigure.data[0].x.length > MAX_POINTS) {
                newFigure.data[0].x = newFigure.data[0].x.slice(-MAX_POINTS);
                newFigure.data[0].y = newFigure.data[0].y.slice(-MAX_POINTS);
                
                newFigure.data[1].x = newFigure.data[1].x.slice(-MAX_POINTS);
                newFigure.data[1].y = newFigure.data[1].y.slice(-MAX_POINTS);
            }
        
            return {data: newFigure.data, layout: newFigure.layout};
        }
        ;//
        ''',
        Output(ids.graph(MATCH), 'figure', allow_duplicate=True),
        Input(ids.sse(MATCH), 'value'),
        State(ids.graph(MATCH), 'figure'),
        prevent_initial_call=True
    )
    
    def __init__(self, chart_type: str, template: str):

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=pd.Series(dtype=object), 
                y=pd.Series(dtype=object), 
                mode="lines+markers",
                name='trace-1',
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=pd.Series(dtype=object), 
                y=pd.Series(dtype=object), 
                mode="lines+markers",
                name='trace-2',
            )
        )
        fig.update_layout(hovermode="x unified")

        fig.update_layout(
            template=template,
            xaxis_title=None,
            title=dict(
                text=chart_type
            ),
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
                SSE(
                    id=self.ids.sse(chart_type), 
                    url=endpoint_url, 
                    options=sse_options(SSEContent(content='please send data')),
                    concat=False,
                ),
                dcc.Graph(
                    id=self.ids.graph(chart_type),
                    figure=fig,
                    style={'height': 450}
                )
            ]
        )


class MantineSSEGraph(html.Div):

    class ids:
        sse = 'mantine-sse'
        graph = 'mantine-graph'

    clientside_callback(
        '''
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
        ''',
        Output(ids.graph, 'data'),
        Input(ids.sse, 'value'),
        State(ids.graph, 'data')
    )

    def __init__(self):
        super().__init__(
            children=[
                SSE(
                    id=self.ids.sse, 
                    url=mantine_endpoint_url, 
                    options=sse_options(SSEContent(content='please send data')), 
                    concat=False
                ),
                dmc.LineChart(
                    id=self.ids.graph,
                    h=300,
                    dataKey="date",
                    data=[],
                    series = [
                        {"name": "Apples", "color": "indigo.6"},
                        {"name": "Oranges", "color": "blue.6"},
                        {"name": "Tomatoes", "color": "teal.6"}
                    ],
                    curveType="linear",
                    tickLine="x",
                    withXAxis=True,
                    withDots=True,
                    lineProps={
                        "isAnimationActive": True,
                        "animationDuration": 500,
                        "animationEasing": "ease-in-out",
                    },
                )

            ]
        )