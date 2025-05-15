import dash_mantine_components as dmc
from dash.development.base_component import Component
from dash.dcc import Graph
import pandas as pd


def create_graph_card_wrapper(graph: Graph, title: str, menu: Component = None, h = 600):
    return dmc.Paper(
        h=h,
        children=dmc.Stack(
            [
                dmc.Group(
                    [dmc.Title(title, order=3), menu],
                    justify="space-between",
                    align="center",
                ),
                dmc.Divider(h=5),
                graph,
            ],
            m="md",
        ),
        withBorder=True,
    )
