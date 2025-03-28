from dash_iconify import DashIconify
from dataclasses import dataclass
from flash import callback, Input, Output, Patch
from dash_router._utils import recursive_to_plotly_json
import plotly.io as pio
import asyncio
import json



def get_icon(icon: str, height: int = 20, *args, **kwargs):
    return DashIconify(icon=icon, height=height, *args, **kwargs)

def create_theme_callback(figure_id):
    @callback(
        Output(figure_id, 'figure', allow_duplicate=True),
        Input('color-scheme-toggle', 'checked'),
        prevent_initial_call=True
    )

    def apply_theme(theme):
        template = pio.templates['plotly_dark'] if theme is True else pio.templates['plotly']
        patch = Patch()
        patch.layout.template = template
        return patch

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


async def flash_props(component_id: str, props):
    """Generate notification props for the specified component ID."""
    # await asyncio.sleep(.1)
    response = [component_id, recursive_to_plotly_json(props)]
    event = ServerSentEvent(json.dumps(response) + '__concatsep__')
    return event.encode()