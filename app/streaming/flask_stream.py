from dash_router.utils.helper_functions import recursive_to_plotly_json
from dash import clientside_callback, Input, Output, State, html, dcc, hooks
from dataclasses import dataclass
from flask import request, make_response, abort
from flask.helpers import stream_with_context
from typing import Callable
import hashlib
import inspect
import json


SSE_CALLBACK_MAP = {}
WS_CALLBACK_MAP = {}

WS_CALLBACK_ENDPOINT = "/stream_dash_update_component"
SSE_CALLBACK_ENDPOINT = "/dash_update_component_sse"

STEAM_SEPERATOR = "__concatsep__"
SSE_CALLBACK_ID_KEY = "sse_callback_id"

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
        return message.encode("utf-8")


class SSECallbackComponent(html.Div):

    class ids:
        sse = "component-update-stream-sse"
        store = "component-update-processing-store"

    def __init__(self):
        super().__init__(
            [
                # SSE(id=self.ids.sse, concat=True, url=SSE_CALLBACK_ENDPOINT),
                # dcc.Store(id=self.ids.store, data={}, storage_type="memory"),
            ]
        )


def generate_clientside_callback(input_ids, sse_callback_id):
    sse_component_id = "component-stream-sse"
    args_str = ", ".join(input_ids)

    property_assignments = [f'    "sse_callback_id": "{sse_callback_id}"']
    for input_id in input_ids:
        property_assignments.append(f'    "{input_id}": {input_id}')

    payload_obj = "{\n" + ",\n".join(property_assignments) + "\n}"

    js_code = f"""
        function({args_str}) {{
            // If no clicks on primary trigger (first argument), return no update
            if ( !window.dash_clientside.callback_context.triggered_id ) {{
                return window.dash_clientside.no_update;
            }}

            // Create payload object with all inputs
            const payload = {{
                ...{payload_obj},
                callback_context: window.dash_clientside.callback_context
            }};
            console.log('Received inputs:', payload);
            // Prepare SSE options with the payload
            const sse_options = {{
                payload: JSON.stringify({{ content: payload }}),
                headers: {{ "Content-Type": "application/json" }},
                method: "POST"
            }};

            console.log(sse_options)
            // Set props for the SSE component
            window.dash_clientside.set_props(
                "{SSECallbackComponent.ids.sse}",
                {{
                    options: sse_options,
                    url: "{SSE_CALLBACK_ENDPOINT}",
                }}
            );
        }}
    """

    return js_code

def generate_deterministic_id(func: Callable, dependencies: tuple) -> str:
        """
        Generates a deterministic SHA256 hash for a callback.
        The hash is based on the function's fully qualified name and a sorted,
        string representation of its dependencies.
        """
        # Ensure the function's identity is part of the hash
        func_identity = f"{func.__module__}.{func.__qualname__}"

        # Create a stable string representation of dependencies.
        # We use repr() for a more exact representation and sort to ensure
        # the order of dependencies doesn't change the hash.
        dependency_reprs = sorted([repr(d) for d in dependencies])
        dependencies_string = ";".join(dependency_reprs)
         # Combine and hash
        unique_string = f"{func_identity}|{dependencies_string}"
        return hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

# @hooks.route(SSE_CALLBACK_ENDPOINT, methods=["POST"])
def sse_component_callback():

    if "text/event-stream" not in request.accept_mimetypes:
        abort(400)

    def send_done_signal(callback_id):
        response = ["[DONE]", {}, callback_id]
        event = ServerSentEvent(json.dumps(response) + STEAM_SEPERATOR)
        return event.encode()

    def send_init_signal(callback_id):
        response = ["[INIT]", {}, callback_id]
        event = ServerSentEvent(json.dumps(response) + STEAM_SEPERATOR)
        return event.encode()

    data = request.get_json()
    content = data["content"].copy()
    ctx = content.pop("callback_context", {})
    callback_id = content.pop(SSE_CALLBACK_ID_KEY)
    callback_func = SSE_CALLBACK_MAP.get(callback_id)

    @stream_with_context
    def callback_generator():
        yield send_init_signal(callback_id)
        for item in callback_func(**content):
            yield item

        yield send_done_signal(callback_id)

    response = make_response(
        callback_generator(),
        {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked",
        },
    )

    response.timeout = None
    return response


# @hooks.layout(priority=1)
# def add_sse_component(layout):
#     return [ SSECallbackComponent()] + layout if isinstance(layout, list) else [SSECallbackComponent(), layout]
#

# hooks.clientside_callback(
#     """ //js
#     function(message, processedData) {
#         if (!message) { return processedData || {} };
#         const DONE_TOKEN = "[DONE]";
#         const INIT_TOKEN = "[INIT]";
#         processedData = processedData || {};
#         const setProps = window.dash_clientside.set_props;
#         const messageList = message.split('__concatsep__');
#
#         // Skip empty messages at the end (from the split)
#         if (messageList[messageList.length - 1] === '') {
#             messageList.pop();
#         }
#
#         // Process only new messages since last time
#         const cbId = JSON.parse(messageList[0])[2]
#         const startIdx = processedData[cbId] || 0;
#         const newMessages = messageList.slice(startIdx);
#         newMessages.forEach(messageStr => {
#             try {
#                 const [componentId, props, callbackId] = JSON.parse(messageStr);
#                 if ( componentId !== DONE_TOKEN && componentId !== INIT_TOKEN ) {
#                     // Set properties on the component
#                     setProps(componentId, props);
#                     processedData[callbackId]++;
#                 }
#
#                 if ( componentId == INIT_TOKEN ) {
#                     processedData[callbackId] = 1
#                 }
#
#                 if ( componentId == DONE_TOKEN) {
#                     processedData[callbackId] = 0
#                 }
#
#             } catch (e) {
#                 console.error("Error processing message:", e, messageStr);
#             }
#         });
#
#         return processedData;
#     }
#     ;// """,
#     Output(SSECallbackComponent.ids.store, "data"),
#     Input(SSECallbackComponent.ids.sse, "value"),
#     State(SSECallbackComponent.ids.store, "data"),
#     prevent_initial_call=True,
# )
#
# hooks.clientside_callback(
#     f"""function ( pathChange ) {{
#         window.dash_clientside.set_props('{SSECallbackComponent.ids.sse}', {{done: true, url: null}});
#         window.dash_clientside.set_props('{SSECallbackComponent.ids.store}', {{data: {{}}}});
#     }}""",
#     Input("_pages_location", "pathname"),
#     prevent_initial_call=True,
# )


def flash_props(component_id: str, props):
    """Generate notification props for the specified component ID."""
    r = request.get_json()
    r_id = r["content"].get(SSE_CALLBACK_ID_KEY)
    response = [component_id, recursive_to_plotly_json(props), r_id]
    event = ServerSentEvent(json.dumps(response) + STEAM_SEPERATOR)
    return event.encode()


def sse_callback(*dependencies, prevent_initital_call=True):

    def decorator(func: Callable) -> Callable:
        # Get function signature to know what arguments it expects
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())
        callback_id = generate_deterministic_id(func, dependencies)
        SSE_CALLBACK_MAP[callback_id] = func

        # Generate and register clientside callback
        clientside_function = generate_clientside_callback(param_names, callback_id)
        clientside_callback(
            clientside_function,
            *dependencies,
            prevent_initial_call=prevent_initital_call,
        )
        # Return the original function unchanged
        return func

    return decorator
