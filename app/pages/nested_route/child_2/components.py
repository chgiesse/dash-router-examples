import dash_ag_grid as dag
from flash import callback, clientside_callback, Input, Output
from .api import get_row_data


class GridTable(dag.AgGrid):

    class ids:
        table = "child-3-table"

    @callback(Output(ids.table, "rowData"), Input(ids.table, "id"))
    async def update_row_data(_):
        data = await get_row_data()
        return data.to_dict("records")

    clientside_callback(
        """
        //js
        function(theme) {
            return theme === false ? 'ag-theme-quartz' : 'ag-theme-quartz-auto-dark';
        }
        ;//
        """,
        Output(ids.table, "className"),
        Input("color-scheme-toggle", "checked"),
    )

    def __init__(self):
        super().__init__(
            id=self.ids.table,
            columnDefs=[
                {"field": "country"},
                {"field": "pop"},
                {"field": "continent"},
                {"field": "lifeExp"},
                {"field": "gdpPercap"},
            ],
            defaultColDef={"filter": True},
            dashGridOptions={
                "animateRows": True,
                "paginationPageSize": 50,
                "pagination": True,
                "loadingOverlayComponent": "CustomLoadingOverlay",
            },
            className="ag-theme-quartz-auto-dark",
            style={"height": "85vh"},
        )
