from flash import Flash, Output

from utils.helpers import create_theme_callback, get_icon
from global_components.notifications import NotificationsContainer
from flash_router import RootContainer
from dash_extensions.streaming import sse_message, sse_options
from dash_extensions import SSE
import json
from quart import request, Response

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


app = Flash(
    __name__,
    # requests_pathname_prefix="/dev/dash/",
    # routes_pathname_prefix="/dev/dash/"
)

payload = {"model": "GPT", "messages": [{'role':'user','content':'tell me a story'}]}

app.layout = dmc.MantineProvider(dmc.Paper([
    dmc.Button("Start Streaming", id="start-btn"),
    SSE(
        id="sse1",
        # url="/stream-openai",
        # options=sse_options(json.dumps(payload)),
        concat=True,
        animate_chunk=5,
        animate_delay=10,
    ),
    dcc.Markdown(id="last_response",style={'font-size':15})
]))

def stream_text(model_name, hist):
    # Simulate streaming text generation
    responses = """
    Once upon a time in a land far, far away,
    there lived a wise old owl. The owl was known throughout \n\n
    the land for its knowledge and kindness. Every day, animals from all over
    would come to the owl to seek advice and learn new **things**. \n\n
    One day, a young rabbit approached the owl with a question about courage. The **owl**
    smiled and began to tell the rabbit a story about bravery and friendship...
    """
    yield responses
    # for response in responses:
    #     yield response + " "
    #     time.sleep(1)  # Simulate delay for streaming effect

@app.server.post("/stream-openai")
async def stream_openai():
    # Accept either raw text or JSON body (sse_options handles both)
    data = await request.get_json()
    print("DATA SSE", data, flush=True)
    if data is None:
        # fallback: raw text (not used here, but keeps parity with your example)
        data = {"messages": [{"role": "user", "content": await request.get_data()}]}

    messages = data.get("messages", [])
    model = data.get("model")

    async def eventStream():
        for piece in stream_text(model_name=model, hist=[{'role':'user','content':'tell me a story'}]):

            yield sse_message(piece)

        yield sse_message("[DONE]")

    return Response(eventStream(), mimetype="text/event-stream")

app.clientside_callback(
    "function(x){return x;}",
    Output("last_response", "children"),
    Input("sse1", "animation"),
)

@app.callback(
    Output("sse1", "url"),
    Output("sse1", "options"),
    Input("start-btn", "n_clicks"),
    prevent_initial_call=True,
)
def start_streaming(_):
    return "/stream-openai", sse_options("Hello, world!")

app.run(debug=True, port=11111)
