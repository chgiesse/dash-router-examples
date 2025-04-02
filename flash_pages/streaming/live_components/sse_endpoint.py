from .components import TestComponentStream
from ..models import ServerSentEvent

from flash import get_app
from quart import request, abort, make_response

app = get_app()

# @app.server.post('/component-sse-stream')
# async def sse_callback():
#     if "text/event-stream" not in request.accept_mimetypes:
#         abort(400)

#     async def callback_generator():
#         # Instead of yielding the generator, iterate through it
#         async for item in TestComponentStream.callback():
#             yield item
        
#         # Add a done marker at the end
#         yield ServerSentEvent(data="[DONE]__concatsep__").encode()
    
#     response = await make_response(
#         callback_generator(),
#         {
#             'Content-Type': 'text/event-stream',
#             'Cache-Control': 'no-cache',
#             'Transfer-Encoding': 'chunked',
#         },
#     )
    
#     response.timeout = None
#     return response