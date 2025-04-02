from helpers import generate_clientside_callback
from dash_router._utils import recursive_to_plotly_json
from flash import Flash, Input, Output, State, clientside_callback
from dash_extensions import SSE
from dash import dcc

from quart import request, abort, make_response
from quart.helpers import stream_with_context
from flash import clientside_callback, html
from dataclasses import dataclass
from uuid import uuid4
import warnings
import inspect
import json


SSE_CALLBACK_MAP = {}
SSE_CALLBACK_ENDPOINT = '/dash_update_component_sse'
STEAM_SEPERATOR = '__concatsep__'
CALLBACK_ID_KEY = 'sse_callback_id'


@dataclass
class ServerSentEvent:
    data: str
    event: str | None = None
    id: int | None = None
    retry: int | None = None

    def encode(self) -> bytes:
        message = f"data: {self.data}"
        if self.event is not None:
            message = f"{message}\nevent: {self.event}"
        if self.id is not None:
            message = f"{message}\nid: {self.id}"
        if self.retry is not None:
            message = f"{message}\nretry: {self.retry}"
        message = f"{message}\n\n"
        return message.encode('utf-8')


class SSECallbackComponent(html.Div):

    class ids:
        sse = 'component-update-stream-sse'
        store = 'component-update-processing-store'

    def __init__(self):
        super().__init__([
            SSE(id=self.ids.sse, concat=True),
            dcc.Store(id=self.ids.store, data={})
        ])


class Streamer:

    def __init__(self, app: Flash):
        self.app = app
        self.server = app.server
        self.setup_component_stream()
        self.setup_processing_callback()

        warnings.warn("""
            This is only for fun purpose! This is not meant
            to be used in any serious sitouation or environment
        """)

    def setup_component_stream(self):

        @self.server.post(SSE_CALLBACK_ENDPOINT)
        async def sse_component_callback():
            if "text/event-stream" not in request.accept_mimetypes:
                abort(400)

            async def send_done_signal(callback_id):
                response = ["[DONE]", {}, callback_id]
                event = ServerSentEvent(json.dumps(response) + STEAM_SEPERATOR)
                return event.encode()

            data = await request.get_json()
            content = data['content'].copy()
            callback_id = content.pop(CALLBACK_ID_KEY)
            callback_func = SSE_CALLBACK_MAP.get(callback_id)

            @stream_with_context
            async def callback_generator():
                
                async for item in callback_func(**content):
                    yield item
                
                yield await send_done_signal(callback_id)
            
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

    def setup_processing_callback(self):

        clientside_callback(
        '''
        //js
        function(message, processedData) {
            if (!message) { return processedData || {} };
            
            const DONE_TOKEN = "[DONE]";
            processedData = processedData || {};
            const setProps = window.dash_clientside.set_props;
            const messageList = message.split('__concatsep__');
            
            // Skip empty messages at the end (from the split)
            if (messageList[messageList.length - 1] === '') {
                messageList.pop();
            }
            
            // Process only new messages since last time
            const cbId = JSON.parse(messageList[0])[2]
            const startIdx = processedData[cbId] || 0;
            const newMessages = messageList.slice(startIdx);
            
            newMessages.forEach(messageStr => {
                try {
                    const [componentId, props, callbackId] = JSON.parse(messageStr);

                    if (componentId !== DONE_TOKEN) {
                        // Set properties on the component
                        setProps(componentId, props);
                        
                        // Track progress for this specific callback ID
                        if (!processedData[callbackId]) {
                            processedData[callbackId] = 0;
                        }
                        processedData[callbackId]++;

                    } else {
                        processedData[callbackId] = 0
                    }
                } catch (e) {
                    console.error("Error processing message:", e, messageStr);
                }
            });
            console.log(processedData)
            return processedData;
        }
        ;//
        ''',
        Output(SSECallbackComponent.ids.store, 'data'),
        Input(SSECallbackComponent.ids.sse, 'value'),
        State(SSECallbackComponent.ids.store, 'data'),
        prevent_initial_call=True
    )


def generate_clientside_callback(input_ids, sse_callback_id):
    args_str = ", ".join(input_ids)
    
    property_assignments = [f'    "{CALLBACK_ID_KEY}": "{sse_callback_id}"']
    for input_id in input_ids:
        property_assignments.append(f'    "{input_id}": {input_id}')
    
    payload_obj = "{\n" + ",\n".join(property_assignments) + "\n}"

    js_code = f'''
        function({args_str}) {{    

            if ( !window.dash_clientside.callback_context.triggered_id ) {{ 
                return window.dash_clientside.no_update;
            }}
            
            // Create payload object with all inputs
            const payload = {payload_obj};
            
            // Prepare SSE options with the payload
            const sse_options = {{
                payload: JSON.stringify({{ content: payload }}),
                headers: {{ "Content-Type": "application/json" }},
                method: "POST"
            }};
            
            // Set props for the SSE component
            window.dash_clientside.set_props(
                "{SSECallbackComponent.ids.sse}",
                {{
                    options: sse_options,
                    url: "{SSE_CALLBACK_ENDPOINT}",
                }}
            );
        }}
    '''   
    
    return js_code
        

def sse_callback(*dependencies, prevent_initital_call=True):
    
    def register_sse_callback(callback_func, callback_map):
        callback_id = str(uuid4())
        callback_map[callback_id] = callback_func
        return callback_id
    
    def decorator(func: callable) -> callable:
        # Get function signature to know what arguments it expects
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())
        
        # Register the original function directly
        callback_id = register_sse_callback(func, SSE_CALLBACK_MAP)
        
        # Generate and register clientside callback
        clientside_function = generate_clientside_callback(param_names, callback_id)
        clientside_callback(clientside_function, *dependencies, prevent_initial_call=prevent_initital_call)
        # Return the original function unchanged
        return func
    
    return decorator


async def flash_props(component_id: str, props):
    """Generate notification props for the specified component ID."""
    r = await request.get_json()
    r_id = r['content'].get(CALLBACK_ID_KEY)
    response = [component_id, recursive_to_plotly_json(props), r_id]
    event = ServerSentEvent(json.dumps(response) + STEAM_SEPERATOR)
    return event.encode()