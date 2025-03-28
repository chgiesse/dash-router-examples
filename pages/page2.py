from dash import dcc, register_page

from .components import LacyContainer

register_page(__name__, path="/page-2")


def layout(**kwargs):
    return LacyContainer(dcc.Loading(display="show"), index=2)
