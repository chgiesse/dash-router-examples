from dash_router import ChildContainer
import dash_mantine_components as dmc


async def layout(children: ChildContainer = None, **kwargs):
    return dmc.Stack([dmc.Title("Files", order=3), children])
