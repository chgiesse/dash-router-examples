import dash_mantine_components as dmc


def layout(cid: str, **kwargs):
    return dmc.Title(f"OM {cid}")
