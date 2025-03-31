from _global_components.notifications import NotificationsContainer
from helpers import flash_props
from ..models import SSEContent, ServerSentEvent

from dash import html, dcc
import dash_mantine_components as dmc
from dash_extensions import SSE
from dash_extensions.streaming import sse_options
from flash import clientside_callback, Input, Output, callback, no_update, State, set_props
from dash_router._utils import recursive_to_plotly_json
from dash._utils import to_json
from dash_iconify import DashIconify
from plotly.express import data
import dash_ag_grid as dag
import pandas as pd
import asyncio
import orjson
import json


class TestComponentStream(dmc.Stack):

    endpoint_url = '/component-sse-stream'

    class ids:
        sse = 'component-stream-sse'
        button = 'stream-button'
        table = 'stream-table'
        store = 'stream-store'

    clientside_callback(
        '''
        //js
        function(message, processedData) {
            if (!message) { return processedData || 0 };

            const DONE_TOKEN = "[DONE]";
            processedData = processedData || 0;
            const setProps = window.dash_clientside.set_props;
            const messageList = message.split('__concatsep__');
            const latestMessageString = messageList.slice(processedData, -1);
            
            const latestData = latestMessageString.map(message => 
                message !== DONE_TOKEN ? JSON.parse(message) : DONE_TOKEN
            );
            
            latestData.forEach(data => {
                if (data !== DONE_TOKEN) {
                    const [componentId, props] = data;
                    setProps(componentId, props);
                    processedData += 1;
                } else {
                    processedData = 0;
                }
            });

            return processedData;
        }  
        ;//
        ''',
        Output(ids.store, 'data'),
        Input(ids.sse, 'value'),
        State(ids.store, 'data'),
        prevent_initial_call=True
    )

    clientside_callback(
        "( theme ) => theme === false ? 'ag-theme-quartz' : 'ag-theme-quartz-auto-dark';",
        Output(ids.table, "className"),
        Input("color-scheme-toggle", "checked"),
    )

    # @callback(
    #     Output(ids.sse, 'options'),
    #     Input(ids.button, 'n_clicks')
    # )
    # def trigger_sse(n_clicks):
    #     if not n_clicks:
    #         return no_update
    #     return sse_options(SSEContent(content=json.dumps({'n_clicks': n_clicks})))


    clientside_callback(
        f'''
        function ( n_clicks ) {{
            console.log('n clcks', n_clicks)
            if ( !n_clicks ) {{ return window.dash_clientside.no_update }}
            const sse_options = {{
                payload: JSON.stringify({{ content: n_clicks }}),
                headers: {{ "Content-Type": "application/json" }},
                method: "POST"
            }}
            window.dash_clientside.set_props(
                "{ids.sse}",
                {{
                    options: sse_options,
                    url: '/component-sse-stream',
                }}
            )
        }}
        ''',
        Input(ids.button, 'n_clicks'),
        prevent_initial_call=True
    )
    
    def __init__(self):
        super().__init__(
            justify='flex-start',
            align='flex-start',
            children=[
                SSE(
                    id=self.ids.sse, 
                    concat=True,
                ),
                dcc.Store(id=self.ids.store, data=0),
                dmc.Button(
                    'Start', 
                    id=self.ids.button, 
                    variant="gradient", 
                    gradient={"from": "grape", "to": "violet", "deg": 35},
                    leftSection=DashIconify(icon='line-md:downloading-loop', height=20),
                    fullWidth=False,
                    styles={'section': {'marginRight': 'var(--mantine-spacing-md)'}}
                ),
                dag.AgGrid(
                    id=self.ids.table,
                    className="ag-theme-quartz-auto-dark",
                    style={'height': '75vh'},
                    dashGridOptions={
                        "pagination": True,
                    }
                )
            ]
        )


from flash import get_app
from quart import request, abort, make_response

app = get_app()

async def callback_test():

    yield await flash_props(TestComponentStream.ids.button, {'loading': True})
    
    df: pd.DataFrame = data.gapminder()
    columnDefs = [{"field": col} for col in df.columns]
    rows_per_step = 500
    total_rows = df.shape[0]

    yield await NotificationsContainer.push_notification(
        title="Started Download!",
        action="show",
        message="Notifications in Dash, Awesome!",
        color='violet'
    )

    yield await flash_props(
        TestComponentStream.ids.table, 
        props={ "columnDefs": columnDefs}
    )

    progress = 0
    while total_rows > 0:

        await asyncio.sleep(2)

        end = len(df) - total_rows + rows_per_step
        total_rows -= rows_per_step
        update_data = df[:end].to_dict("records")
        df.drop(df.index[:end], inplace=True)
        update_props = (
            {"rowTransaction": {"add": update_data}}
            if progress > 0 else 
            {"rowData": update_data}
        )

        yield await flash_props(
            TestComponentStream.ids.table,
            update_props
        )
        
        progress += 1
        
    
    yield await flash_props(
        TestComponentStream.ids.button, 
        {
            'loading': False, 
            'leftSection': DashIconify(icon='famicons:reload-circle', height=20),
            'children': 'Reload',
        }
    )

    yield await NotificationsContainer.push_notification(
        title="Finished Callback!",
        action="show",
        message="Notifications in Dash, Awesome!",
        icon=DashIconify(icon="akar-icons:circle-check"),
        color='lime',
    )

@app.server.post('/component-sse-stream')
async def sse_callback():
    if "text/event-stream" not in request.accept_mimetypes:
        abort(400)

    load_data = await request.get_json()
    async def callback_generator():
        # Instead of yielding the generator, iterate through it
        async for item in callback_test():
            yield item
        
        # Add a done marker at the end
        yield ServerSentEvent(data="[DONE]__concatsep__").encode()
    
    response = await make_response(
        callback_generator(),
        {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )
    
    response.timeout = None
    return response