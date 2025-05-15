from .api import get_data
from global_components.notifications import NotificationsContainer
from streaming.stream import flash_props, sse_callback

from dash import dcc
import dash_mantine_components as dmc
from dash_extensions import SSE
from flash import clientside_callback, Input, Output
from dash_iconify import DashIconify
import dash_ag_grid as dag


class TestComponentStream(dmc.Stack):

    class ids:
        button = "stream-button"
        table = "stream-table"

    theme_csc = clientside_callback(
        "( theme ) => theme === false ? 'ag-theme-quartz' : 'ag-theme-quartz-auto-dark';",
        Output(ids.table, "className"),
        Input("color-scheme-toggle", "checked"),
    )

    @sse_callback(Input(ids.button, "n_clicks"))
    async def update_table(n_clicks):

        yield await flash_props(TestComponentStream.ids.button, {"loading": True})

        yield await NotificationsContainer.push_notification(
            title="Starting Download!",
            action="show",
            message="Notifications in Dash, Awesome!",
            color="lime",
        )

        progress = 0
        chunck_size = 500
        async for data_chunk, colnames in get_data(chunck_size):
            update = {"rowTransaction": {"add": data_chunk}}
            if progress == 0:
                update = {"rowData": data_chunk}
                columnDefs = [{"field": col} for col in colnames]
                yield await flash_props(
                    TestComponentStream.ids.table, props={"columnDefs": columnDefs}
                )

            yield await flash_props(TestComponentStream.ids.table, update)

            if len(data_chunk) == chunck_size:
                yield await NotificationsContainer.push_notification(
                    title="Progress",
                    action="show",
                    message=f"Processed {chunck_size + (chunck_size * progress)} items",
                    color="violet",
                )

            progress += 1

        yield await flash_props(
            TestComponentStream.ids.button,
            {
                "loading": False,
                # 'leftSection': DashIconify(icon='famicons:reload-circle', height=20),
                "children": "Reload",
            },
        )

        yield await NotificationsContainer.push_notification(
            title="Finished Callback!",
            action="show",
            message="Notifications in Dash, Awesome!",
            icon=DashIconify(icon="akar-icons:circle-check"),
            color="lime",
        )

    def __init__(self):
        super().__init__(
            justify="flex-start",
            align="flex-start",
            children=[
                dmc.Button(
                    "Start",
                    id=self.ids.button,
                    variant="gradient",
                    gradient={"from": "grape", "to": "violet", "deg": 35},
                    leftSection=DashIconify(
                        icon="material-symbols:download-rounded", height=20
                    ),
                    fullWidth=False,
                    styles={"section": {"marginRight": "var(--mantine-spacing-md)"}},
                ),
                dag.AgGrid(
                    id=self.ids.table,
                    className="ag-theme-quartz-auto-dark",
                    style={"height": "75vh"},
                    dashGridOptions={
                        "pagination": True,
                    },
                ),
            ],
        )
