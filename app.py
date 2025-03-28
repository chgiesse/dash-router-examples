from dash import Dash, html, page_container, dcc, callback, MATCH, Input, Output
from pages.components import LacyContainer
import time

app = Dash(__name__, use_pages=True)

col_style = {
    "display": "flex",
    "flexDirection": "column",
    "gap": "2rem",
}

row_style = {
    "display": "flex", 
    "flexDirection": "row", 
    "gap": "4rem", 
    "margin": "2rem"
}

app.layout = html.Div(
    style=row_style,
    children=[
        html.Div(
            style=col_style,
            children=[
                dcc.Link("Page - 1", href="/page-1"),
                dcc.Link("Page - 2", href="/page-2"),
            ]
        ),
        html.Div(page_container),
    ],
)

@callback(
    Output(LacyContainer.ids.container(MATCH), "children"),
    Input(LacyContainer.ids.container(MATCH), "id")
)

def load_lacy(lacy_id):
    time.sleep(1.3)
    lacy_index = lacy_id.get('index')
    children = (
        html.Div(
            children=[
                html.Div(lacy_index),
                LacyContainer(dcc.Loading(display="show"), index=3),     
            ],
            style=col_style
        )
        if lacy_index < 4 else
        html.Div(
            lacy_index
        )
    )

    return children

if __name__ == "__main__":
    app.run(debug=True, port=3000)
