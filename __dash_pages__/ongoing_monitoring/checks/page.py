import dash_mantine_components as dmc

from dash_router import RouteConfig

config = RouteConfig(path_template="<cid>", is_static=True)


def layout(cid: str, **kwargs):
    return dmc.Title(f"OM {cid}")
