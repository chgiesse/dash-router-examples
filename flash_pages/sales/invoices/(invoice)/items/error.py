import dash_mantine_components as dmc


async def layout(e: Exception, *args, **kwargs):
    return dmc.Alert(str(e), title="Error occured", color="red", variant="light")
