from global_components.notifications import NotificationsContainer
from global_components.theme import ThemeComponent
from utils.helpers import parse_qs
from .api import endpoint
from ..models import SalesCallbackParams, sales_variant_type
from ..components.menu import GraphMenu

from dash_router import RootContainer
import dash_mantine_components as dmc
from flash import callback, Input, Output, State, no_update, ctx, clientside_callback
from dash_ag_grid import AgGrid
from dash import dcc
import plotly.express as px
import pandas as pd


class TotalSalesGraph(dmc.AreaChart):
    """Total Sales Graph implemented with Dash Mantine Components."""

    title = "Total Sales over Time"

    class ids:
        graph = "amazon-total-sales-graph"
        table = "amazon-total-sales-table"
        relative_switch = "amazon-total-sales-rel-switch"
        table_switch = "amazon-total-sales-tbl-switch"
        running_switch = "amazon-total-sales-run-switch"
        variant_select = "amazon-total-sales-var-select"

    clientside_callback(
        f"""( hideTable ) => {{
            document.querySelector('.{ids.table}').setAttribute('data-hidden', !hideTable);
            document.querySelector('.{ids.graph}').setAttribute('data-hidden', hideTable);
        }}""",
        Input(ids.table_switch, "checked"),
    )

    @callback(
        Output(ids.graph, "data"),
        Output(ids.table, "rowData"),
        Input(ids.relative_switch, "checked"),
        Input(ids.running_switch, "checked"),
        Input(ids.variant_select, "value"),
        State(RootContainer.ids.location, "search"),
        State(ThemeComponent.ids.store, "data"),
        running=[
            (Output(GraphMenu.ids.trigger_button(ids.graph), "loading"), True, False)
        ],
        prevent_initial_call=True,
    )
    async def update(
        is_relative: bool,
        is_running: bool,
        variant: sales_variant_type,
        qs: str,
        is_darkmode: bool,
    ):
        try:
            query_params = parse_qs(qs)
            sales_params = SalesCallbackParams(
                variant=variant, is_relative=is_relative, is_running=is_running
            )
            data = await endpoint(**query_params, variant=sales_params.variant)

        except Exception as e:
            NotificationsContainer.send_notification(
                title="Data fetching error",
                message=str(e),
                color="red",
            )
            return no_update, no_update

        triggered_id = ctx.triggered_id
        if is_relative and triggered_id == TotalSalesGraph.ids.relative_switch:
            data = data.divide(data.sum(axis=1), axis=0).round(3).fillna(0)

        if is_running and triggered_id == TotalSalesGraph.ids.running_switch:
            data = data.cumsum()

        chart_data = TotalSalesGraph.prepare_chart_data(data)
        row_data = data.T.reset_index(names="Category").to_dict(orient="records")

        return chart_data, row_data

    @staticmethod
    def prepare_chart_data(data: pd.DataFrame):
        chart_data = data.reset_index(names="dataKey").to_dict(orient="records")
        return chart_data

    @staticmethod
    def figure(data: pd.DataFrame):
        series = []
        colors = ["violet.6", "blue.6", "teal.6", "red.6", "green.6", "orange.6"]

        for i, col in enumerate(data.columns):
            series.append({
                "name": col,
                "color": colors[i % len(colors)],
                "stackId": "stack1"  # Add stackId for stacking
            })

        data = data.fillna(0)
        chart_data = data.reset_index(names="date").to_dict(orient="records")

        for record in chart_data:
            for key in record:
                if record[key] is None or pd.isna(record[key]):
                    record[key] = 0

        chart_config = {
            "data": chart_data,
            "dataKey": "date",
            "series": series,
            "withLegend": True,
            "legendProps": {"verticalAlign": "bottom"},
            "withXAxis": True,
            "withYAxis": True,
            "yAxisProps": {"width": 50},
            "areaProps": {"isAnimationActive": True}  # Changed from barProps to areaProps
        }

        return chart_config

    @classmethod
    def table(cls, data: pd.DataFrame):
        data = data.T.reset_index(names="Category")
        columnDefs = [
            {"field": "Category", "pinned": "left", "width": 180, "filter": True}
        ]
        columnDefs += [
            {"field": col, "width": 110, "filter": False} for col in data.columns[1:]
        ]

        table = AgGrid(
            id=cls.ids.table,
            rowData=data.to_dict(orient="records"),
            columnDefs=columnDefs,
            defaultColDef={"filter": False},
            className="ag-theme-quartz-auto-dark card-bg",
            dashGridOptions={"rowHeight": 55},
        )
        return table

    def __init__(self, data: pd.DataFrame):
        chart_config = self.figure(data)

        super().__init__(
            id=self.ids.graph,
            h=500,
            # type="area",  # Set chart type to area
            # highlightHover=False,
            # className="fade-in-chart",
            # className="fade-in-bottom",
            **chart_config,
        )
