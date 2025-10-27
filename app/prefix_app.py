# import time

# from dash_extensions import SSE
# from dash import dcc
# from dash_extensions.enrich import DashProxy, Input, Output, html
# from dash_extensions.streaming import sse_message, sse_options
# from flask import Response, request

# # Create a small example app.
# app = DashProxy(__name__)
# app.layout = html.Div(
#     [
#         html.Button("Start streaming", id="btn"),
#         SSE(id="sse", concat=True),
#         dcc.Markdown(id="response", style={"whiteSpace": "pre-wrap"}),
#     ]
# )
# # Render (concatenated, animated) text from the SSE component.
# app.clientside_callback(
#     "function(x){return x};",
#     Output("response", "children"),
#     Input("sse", "value"),
# )


# @app.callback(
#     Output("sse", "url"),
#     Output("sse", "options"),
#     Input("btn", "n_clicks"),
#     prevent_initial_call=True,
# )
# def start_streaming(_):
#     return "/stream", sse_options("Hello, world!")


# @app.server.post("/stream")
# def stream():
#     message = request.data.decode("utf-8")

#     def eventStream():
#         yield sse_message(message)
#         yield sse_message("more text coming up...")
#         # for char in message:
#         #     time.sleep(0.1)
#         #     yield sse_message(char)
#         # yield sse_message()

#     return Response(eventStream(), mimetype="text/event-stream")


# app.run(debug=True, port=11111)
from flash import Input, event_callback, stream_props, page_container
# from utils.risklab import build_root_path, getPort, setProd, setPort
from flash import Flash
import dash_mantine_components as dmc
import pandas as pd
import asyncio
import plotly
import dash_ag_grid as dag

# setPort(8058)
# setProd(False)

app = Flash(
    __name__,
    update_title="Updating...",
    # requests_pathname_prefix=build_root_path(port=getPort()),
    requests_pathname_prefix="/dev/",
    routes_pathname_prefix="/dev/",
    # use_pages=True,
    # pages_folder="qpages",
    # suppress_callback_exceptions=True,
)

app.layout = dmc.MantineProvider(
    [
        dmc.Button("Start stream", id="start-stream-button"),
        dmc.Button("Cancel stream", id="cancel-stream-button", display="None"),
        dag.AgGrid(id="dash-ag-grid")
    ]
)

async def get_data(chunk_size: int):
    df: pd.DataFrame = plotly.data.gapminder()
    total_rows = df.shape[0]

    while total_rows > 0:
        await asyncio.sleep(2)
        end = len(df) - total_rows + chunk_size
        total_rows -= chunk_size
        update_data = df[:end].to_dict("records") # type: ignore
        df.drop(df.index[:end], inplace=True) # type: ignore
        yield update_data, df.columns

@event_callback(Input("start-stream-button", "n_clicks"))
async def update_table(_):

    yield stream_props([
        ("start-stream-button", {"loading": True}),
        ("cancel-stream-button", {"display": "flex"})
    ])

    progress = 0
    chunk_size = 500
    async for data_chunk, colnames in get_data(chunk_size):
        if progress == 0:
            columnDefs = [{"field": col} for col in colnames]
            update = {"rowData": data_chunk, "columnDefs": columnDefs}
        else:
            update = {"rowTransaction": {"add": data_chunk}}

        yield stream_props("dash-ag-grid", update)

        progress += 1

    yield stream_props("start-stream-button", {"loading": False, "children": "Reload"})
    yield stream_props("reset-strea-button", {"display": "none"})

if __name__ == "__main__":
    app.run(port=8058, debug=True, dev_tools_hot_reload=False)
