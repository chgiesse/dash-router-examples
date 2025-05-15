from ..models import ServerSentEvent
from quart import make_response, abort, request
from dash._utils import to_json
from flash import get_app
from datetime import datetime
import asyncio
import random
import time

app = get_app()

endpoint_url = "/test-sse"
mantine_endpoint_url = "/test-sse-mantine"


@app.server.post(endpoint_url)
async def sse():
    if "text/event-stream" not in request.accept_mimetypes:
        abort(400)

    async def send_events():
        start_time = time.time()
        multiplicator = 1
        rounds = 0

        while True:
            await asyncio.sleep(0.5)

            # Calculate elapsed time in seconds
            elapsed_time = time.time() - start_time
            print("Elapsed time: ", round(elapsed_time, 0), flush=True)
            # Generate random values
            y1 = random.random() * multiplicator
            y2 = random.random() * multiplicator

            # Add 1 to values after 10 seconds
            if int(elapsed_time) % 10 == 0:
                multiplicator = random.randint(-1, 1) * rounds + 1
                rounds += 1

            x = datetime.now()
            data = dict(x=x, y1=y1, y2=y2)
            event = ServerSentEvent(to_json(data))
            yield event.encode()

    response = await make_response(
        send_events(),
        {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked",
        },
    )
    response.timeout = None
    return response


@app.server.post(mantine_endpoint_url)
async def mantine_sse():
    if "text/event-stream" not in request.accept_mimetypes:
        abort(400)

    async def send_events():
        while True:
            await asyncio.sleep(1)
            data = dict(
                date=datetime.now(),
                Tomatoes=random.randint(900, 3000),
                Oranges=random.randint(900, 3000),
                Apples=random.randint(900, 3000),
            )

            event = ServerSentEvent(to_json(data))
            yield event.encode()

    response = await make_response(
        send_events(),
        {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked",
        },
    )
    response.timeout = None
    return response
