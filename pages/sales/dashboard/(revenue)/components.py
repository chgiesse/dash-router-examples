from global_components.notifications import NotificationsContainer
from global_components.theme import ThemeComponent
from global_components.location import Url
from utils.helpers import parse_qs, get_theme_template
from utils.constants import common_figure_config
from .api import endpoint
from ..models import SalesCallbackParams, sales_variant_type

from dash_router import RootContainer
from flash import callback, Input, Output, State, no_update, ctx, clientside_callback
from dash_ag_grid import AgGrid
from dash import dcc
import plotly.express as px
import pandas as pd


class TotalSalesGraph(dcc.Graph):

    title = "Total Sales over Time"

    class ids:
        graph = "amazon-total-sales-graph"
        table = "amazon-total-sales-table"
        relative_switch = "amazon-total-sales-rel-switch"
        table_switch = "amazon-total-sales-tbl-switch"
        running_switch = "amazon-total-sales-run-switch"
        variant_select = "amazon-total-sales-var-select"

    # GraphMenu.download_callback(ids.graph)
    # ThemeComponent.graph_theme_callback(ids.graph)
    clientside_callback(
        f"""( hideTable ) => {{
            document.querySelector('.{ids.table}').setAttribute('data-hidden', !hideTable);
            document.querySelector('.{ids.graph}').setAttribute('data-hidden', hideTable);
        }}""",
        Input(ids.table_switch, "checked"),
    )

    @callback(
        Output(ids.graph, "figure"),
        Output(ids.table, "rowData"),
        Input(ids.relative_switch, "checked"),
        Input(ids.running_switch, "checked"),
        Input(ids.variant_select, "value"),
        State(RootContainer.ids.location, "search"),
        State(ThemeComponent.ids.toggle, "checked"),
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
                title="Data fetching errror",
                message=str(e),
                color="red",
            )
            return no_update

        triggered_id = ctx.triggered_id
        if is_relative and triggered_id == TotalSalesGraph.ids.relative_switch:
            data = data.divide(data.sum(axis=1), axis=0).round(3).fillna(0)

        if is_running and triggered_id == TotalSalesGraph.ids.running_switch:
            data = data.cumsum()

        fig = TotalSalesGraph.figure(data, is_darkmode)
        row_data = data.T.reset_index(names="Category").to_dict(orient="records")

        return fig, row_data

    @staticmethod
    def figure(data: pd.DataFrame, is_darkmode: bool):
        fig = px.bar(data, text_auto=True)
        template = get_theme_template(is_darkmode)
        fig.update_layout(
            **common_figure_config,
            margin=dict(l=0, r=0, t=0, b=0),
            uirevision=True,
            template=template,
        )
        return fig

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

    def __init__(self, data: pd.DataFrame, is_darkmode: bool):
        fig = self.figure(data, is_darkmode)

        super().__init__(
            figure=fig, config={"displayModeBar": False}, id=self.ids.graph
        )
