from dash_iconify import DashIconify
from urllib.parse import parse_qs as base_parse_qs
from flash import callback, Input, Output, Patch, ctx
from pathlib import Path
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
        def create_patch():
            patched_fig = Patch()
            patched_fig["layout"]["template"] = template
            return patched_fig

        if isinstance(ctx.outputs_list, list):
            return [create_patch() for _ in ctx.outputs_list]

        return create_patch()


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


def bundle_css(input_dir, output_file="bundled_styles.css"):
    """
    Concatenate all .css files from input_dir into one file in the assets folder.
    Dash will automatically serve the bundled file from the assets folder.
    """
    css_dir = Path(input_dir)
    print(f"Bundling CSS files from {css_dir} into {output_file}...", flush=True)
    css_files = sorted(css_dir.glob("*.css"))  # sort for deterministic order

    # Get the app directory relative to this file's location
    app_dir = Path(__file__).parent.parent  # from app/utils/helper_functions.py -> app/
    assets_dir = app_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    output_path = assets_dir / output_file
    print(f"Output path: {output_path}", flush=True)

    with open(output_path, "w", encoding="utf-8") as outfile:
        for css_file in css_files:
            outfile.write(f"/* {css_file.name} */\n")
            outfile.write(css_file.read_text(encoding="utf-8"))
            outfile.write("\n\n")

    print(f"Bundled {len(css_files)} CSS files into {output_path}")
