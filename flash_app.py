import dash_mantine_components as dmc
from aiocache import Cache
from dash_router import RootContainer, Router
from flash import Flash, State, Input, callback, no_update, Output
from flash._pages import _parse_path_variables, _parse_query_string

import importlib
from appshell import create_appshell
from streaming.stream import SSECallbackComponent, Streamer
from theme import apply_vizro_theme


app = Flash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dmc.styles.CHARTS,
        dmc.styles.DATES,
        dmc.styles.NOTIFICATIONS,
        dmc.styles.RICH_TEXT_EDITOR,
    ],
    external_scripts=["https://unpkg.com/hotkeys-js/dist/hotkeys.min.js"],
    pages_folder="flash_pages",
    use_pages=False,
    update_title=None,
    routing_callback_inputs={"theme": State("color-scheme-toggle", "checked")},
)


app.layout = create_appshell([RootContainer(), SSECallbackComponent()])

router = Router(app)
streamer = Streamer(app)
cache = Cache()

apply_vizro_theme()

# @callback(
#     # Output(RootContainer.ids.dummy, 'children', allow_duplicate=True),
#     Input(RootContainer.ids.location, 'search'),
#     State(RootContainer.ids.location, 'pathname'),
#     State(RootContainer.ids.state_store, 'data'),
#     prevent_initial_call=True
# )   
# async def query_params(_search, _pathname, _loading_state):
#     query_parameters = _parse_query_string(_search)
#     print('Search: ', query_parameters, flush=True)
#     # return no_update



if __name__ == "__main__":
    app.run(debug=True, port=8031)
