import dash_mantine_components as dmc

from dash_router import RouteConfig

config = RouteConfig(is_static=True)


def layout(**kwargs):
    return dmc.Title("OM History")
