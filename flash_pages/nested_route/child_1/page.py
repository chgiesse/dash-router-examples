import dash_mantine_components as dmc


async def layout(*args, **kwargs):
    return dmc.Box(dmc.Title("Child 1", w=300))
