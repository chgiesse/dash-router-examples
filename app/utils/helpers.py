from dash_iconify import DashIconify
from urllib.parse import parse_qs as base_parse_qs
from flash import callback, Input, Output, Patch
import plotly.io as pio


def parse_qs(query_string, *args, **kwargs):
    query_string = query_string.split("?")[-1]
    parsed = base_parse_qs(query_string, *args, **kwargs)
    return {key: values[0] if values else "" for key, values in parsed.items()}


def get_theme_template(is_darkmode: bool):
    return "plotly_dark" if is_darkmode else "plotly"


def get_icon(icon: str, height: int = 20, *args, **kwargs):
    return DashIconify(icon=icon, height=height, *args, **kwargs)


def create_theme_callback(figure_id):
    @callback(
        Output(figure_id, "figure"),
        Input("color-scheme-toggle", "checked"),
        prevent_initial_call=True,
    )
    def apply_theme(theme):
        template = (
            pio.templates["plotly_dark"] if theme is True else pio.templates["plotly"]
        )
        patched_fig = Patch()
        patched_fig["layout"]["template"] = template
        return patched_fig


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
            console.log('Received inputs:', {{{args_str}}});
            
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
                "{sse_component_id}",
                {{
                    options: sse_options,
                    url: '/component-sse-stream',
                }}
            );
        }}
    """

    return js_code
