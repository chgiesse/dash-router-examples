# from dash import Dash, Input, Output, State  # , _dash_renderer, Dash
import dash_mantine_components as dmc
from global_components.appshell import create_appshell
from dash import Dash, State
from theme import apply_vizro_theme
from dash_router import RootContainer, Router

# from pages.sales.page import layout


# _dash_renderer._set_react_version("18.2.0")
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    routing_callback_inputs={"theme": State("color-scheme-toggle", "checked")},
)
# app = Dash(__name__)
router = Router(app, pages_folder="dash_pages",)
apply_vizro_theme()

app.layout = create_appshell([RootContainer()])

if __name__ == "__main__":
    app.run(debug=True, port=8032)
