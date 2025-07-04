import dash_mantine_components as dmc
from aiocache import Cache
# from dash_router import RootContainer, Router
# from dash_router import Router, RootContainer
from flash_router import FlashRouter, RootContainer
from flash import Flash, State, Input, callback, no_update, Output

import importlib
from global_components.appshell import create_appshell
from streaming.stream import SSECallbackComponent, Streamer
from theme import apply_vizro_theme
# from api.sql_operator import setup_db


app = Flash(
    __name__,
    suppress_callback_exceptions=True,
    external_scripts=["https://unpkg.com/hotkeys-js/dist/hotkeys.min.js"],
    pages_folder="pages",
    use_pages=False,
    update_title=None,
    routing_callback_inputs={"theme": State("color-scheme-toggle", "checked")},
    compress=True
)

app.layout = create_appshell([RootContainer(), SSECallbackComponent()])

server = app.server
# server.before_serving(setup_db)

router = FlashRouter(app)
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
