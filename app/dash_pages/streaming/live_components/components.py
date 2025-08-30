from .api import get_data
from global_components.notifications import NotificationsContainerSync
from dash_event_callback import event_callback, stream_props

import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_ag_grid as dag
from dash import Input


class TestComponentStream(dmc.Stack):

    class ids:
        button = "stream-button"
        table = "stream-table"

    @event_callback(Input(ids.button, "n_clicks"))
    def update_table(n_clicks):

        yield stream_props(TestComponentStream.ids.button, {"loading": True})

        yield NotificationsContainerSync.push_notification(
            title="Starting Download!",
            message="Notifications in Dash, Awesome!",
            color="lime",
        )

        progress = 0
        chunck_size = 500
        for data_chunk, colnames in get_data(chunck_size):
            update = {"rowTransaction": {"add": data_chunk}}
            if progress == 0:
                update = {"rowData": data_chunk}
                columnDefs = [{"field": col} for col in colnames]
                yield stream_props(
                    TestComponentStream.ids.table, {"columnDefs": columnDefs}
                )

            yield stream_props(TestComponentStream.ids.table, update)

            if len(data_chunk) == chunck_size:
                yield NotificationsContainerSync.push_notification(
                    title="Progress",
                    message=f"Processed {chunck_size + (chunck_size * progress)} items",
                    color="violet",
                )

            progress += 1

        yield stream_props(
            TestComponentStream.ids.button,
            {
                "loading": False,
                "children": "Reload",
            },
        )

        yield NotificationsContainerSync.push_notification(
            title="Finished Callback!",
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
