# from dash import Dash, Input, Output, State  # , _dash_renderer, Dash
import dash_mantine_components as dmc
from global_components.appshell import create_appshell
from dash import Dash

from dash_router import RootContainer, SyncRouter

# from pages.sales.page import layout


# _dash_renderer._set_react_version("18.2.0")
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dmc.styles.CHARTS],
    pages_folder="dash_pages",
)
# app = Dash(__name__)
router = SyncRouter(app)

app.layout = create_appshell([RootContainer()])

if __name__ == "__main__":
    app.run(debug=True, port=8032)
