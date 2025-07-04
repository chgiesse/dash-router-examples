import dash_mantine_components as dmc
from dash_iconify import DashIconify


async def layout(*args, **kwargs):
    return dmc.Alert(
        children=[
            dmc.Text("Oops a error ocured:", c="dimmed", w=700, size="md"),
            dmc.Text(f"Error {args[0]}", size="xs"),
            dmc.Text(f"Variables {args[1:]}", size="xs"),
        ],
        title="Error!!!",
        color="red",
        variant="outline",
        icon=DashIconify(icon="material-symbols:cancel-outline-rounded"),
        maw="100%",
    )
