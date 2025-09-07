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
    router=FlashRouter,
    handle_theme=True,
)

app.layout = create_appshell([
    RootContainer(),
])

# @hooks.index()
# def add_meta(index):
#     index = index.replace("<head>", "<head>" + '''
#         <meta name="viewport" content="width=device-width, initial-scale=1">
#         <link rel="icon" type="image/png" href="/assets/favicon.png">
#         <link rel="preconnect" href="https://fonts.googleapis.com">
#         <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#         <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
#         <style>
#             body {
#                 font-family: 'Inter', sans-serif;
#             }
#         </style>
#     '''
# )
#     return index

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

cache = Cache()
apply_vizro_theme()
# setup_metrics(app)
# router = FlashRouter(app, requests_pathname_prefix="/dev/")

if __name__ == "__main__":
    app.run(debug=True, dev_tools_ui=False, port=8031)
