import dash_mantine_components as dmc
from aiocache import Cache
# from dash_router import RootContainer, Router
# from dash_router import Router, RootContainer
from flash_router import FlashRouter, RootContainer
from flash import Flash, State, Input, callback, no_update, Output, hooks

import importlib
from global_components.appshell import create_appshell
from theme import apply_vizro_theme
# from api.sql_operator import setup_db
from monitoring.metrics import setup_metrics


app = Flash(
    __name__,
    suppress_callback_exceptions=True,
    pages_folder="pages",
    use_pages=False,
    update_title=None,  # type: ignore[arg-type]
    routing_callback_inputs={"theme": State("color-scheme-toggle", "checked")},
    compress=True,
)

app.layout = create_appshell([
    RootContainer(),
])

server = app.server
# server.before_serving(setup_db)


# app.clientside_callback(
#     """
#     function(checked){
#         var scheme = checked ? 'dark' : 'light';
#         if (typeof window.setMantineScheme === 'function') {
#             window.setMantineScheme(scheme);
#         }
#         return scheme;
#     }
#     """,
#     Output(theme_template, "data"),
#     Input("color-scheme-toggle", "checked"),
# )

router = FlashRouter(app)
cache = Cache()
apply_vizro_theme()
# setup_metrics(app)

if __name__ == "__main__":
    app.run(debug=True, port=8031)
