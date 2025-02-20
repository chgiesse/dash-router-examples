import dash_mantine_components as dmc

from dash_router import RouteConfig

config = RouteConfig(is_static=True, path_template="<test_1>/test/<test_2>")


def layout(test_1=None, test_2=None, **kwargs):
    return dmc.Title(f"OM Overview {test_1} {test_2}")
