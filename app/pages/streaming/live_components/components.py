from global_components.notifications import NotificationsContainer
from flash_router import RootContainer
from .api import get_data

from flash import Input, stream_props, event_callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_ag_grid as dag


class TestComponentStream(dmc.Stack):

    class ids:
        start_btn = "stream-button-test"
        cancel_btn = "cancel-button-test"
        table = "stream-table"

    @event_callback(
        Input(ids.start_btn, "n_clicks", allow_optional=True),
        cancel=[
            (Input(RootContainer.ids.location, "pathname"), "/streaming/live-components"),
            (Input(ids.cancel_btn, "n_clicks", allow_optional=True), 0)
        ],
        reset_props=[
            (ids.table, {"rowData": [], "columnDefs": []}),
            (ids.start_btn, {"children": "Download Data", "loading": False}),
            (ids.cancel_btn, {"display": "none"}),
        ],
        prevent_initial_call=False
    )
    async def update_table(_ = None):

        # batch set loading on both buttons
        yield stream_props([
            (TestComponentStream.ids.start_btn, {"loading": True}),
            (TestComponentStream.ids.cancel_btn, {"display": "flex"}),
        ])

        progress = 0
        chunck_size = 500
        async for data_chunk, colnames in get_data(chunck_size):
            if progress == 0:
                columnDefs = [{"field": col} for col in colnames]
                update = {"rowData": data_chunk, "columnDefs": columnDefs}
            else:
                update = {"rowTransaction": {"add": data_chunk}}

            # use batched stream_props (single-item list) for consistency
            yield stream_props([(TestComponentStream.ids.table, update)])
            progress += 1

        # batch reset both buttons
        yield stream_props([
            (TestComponentStream.ids.start_btn, {"loading": False, "children": "Reload"}),
            (TestComponentStream.ids.cancel_btn, {"display": "none"}),
        ])

        yield NotificationsContainer.send_notification(
            title="Finished Callback!",
            message="Notifications in Dash, Awesome!",
            icon=DashIconify(icon="akar-icons:circle-check"),
            color="lime",
            position="bottom-right",
        )

    def __init__(self):

        download_button = dmc.Button(
            "Download Data",
            id=self.ids.start_btn,
            leftSection=DashIconify(
                icon="material-symbols:download-rounded", height=20
            ),
            fullWidth=False,
            styles={"section": {"marginRight": "var(--mantine-spacing-md)"}},
        )

        cancel_button = dmc.Button(
            "Cancel Download",
            id=self.ids.cancel_btn,
            leftSection=DashIconify(icon="mingcute:stop-circle-line", height=15),
            fullWidth=False,
            styles={"section": {"marginRight": "var(--mantine-spacing-md)"}},
            color="red",
            variant="outline",
            display="none",
        )

        super().__init__(
            [
                dmc.Group(
                    [cancel_button, download_button],
                    justify="flex-end",
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
            justify="flex-end",
        )
