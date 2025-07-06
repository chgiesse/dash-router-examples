import dash_mantine_components as dmc
from aiocache import Cache
from flash_router import RootContainer, FlashRouter
from flash import Flash, State

from global_components.appshell import create_appshell
from streaming.stream import SSECallbackComponent, Streamer
from theme import apply_vizro_theme
from api.sql_operator import setup_db


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
    pages_folder="pages",
    use_pages=False,
    update_title=None,
    routing_callback_inputs={"theme": State("color-scheme-toggle", "checked", allow_optional=True)},
)

app.layout = create_appshell([RootContainer(), SSECallbackComponent()])

server = app.server
# server.before_serving(setup_db)

router = FlashRouter(app)
streamer = Streamer(app)
cache = Cache()
apply_vizro_theme()
