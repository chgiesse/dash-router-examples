from appshell import create_appshell
from streaming.stream import Streamer, SSECallbackComponent
from theme import add_figure_templates
import dash_mantine_components as dmc
from aiocache import Cache
from dash._utils import inputs_to_vals
from dash_router import RootContainer, Router, PageNode
from dash_router.components import LacyContainer
from flash import MATCH, Flash, Input, Output, State, callback
from flash._pages import _parse_query_string
from quart import request
from uuid import UUID
import json


app = Flash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dmc.styles.CHARTS, dmc.styles.DATES, dmc.styles.NOTIFICATIONS, dmc.styles.RICH_TEXT_EDITOR], 
    external_scripts=["https://unpkg.com/hotkeys-js/dist/hotkeys.min.js"],
    pages_folder="flash_pages",
    use_pages=False,
    update_title=None,
    routing_callback_inputs={
        "theme": State("color-scheme-toggle", "checked")
    }
)
router = Router(app)
streamer = Streamer(app)
app.layout = create_appshell([RootContainer(), SSECallbackComponent()])
cache = Cache()

add_figure_templates(default="mantine_dark")

@callback(
    Output(LacyContainer.ids.container(MATCH), "children"),
    Input(LacyContainer.ids.container(MATCH), "id"),
    Input(LacyContainer.ids.container(MATCH), "data-path"),
    State(RootContainer.ids.location, "pathname"),
    State(RootContainer.ids.location, "search"),
    State(RootContainer.ids.state_store, "data"),
)
async def load_lacy_component(
    lacy_segment_id, variables, pathname, search, loading_state
):
    request_data = await request.get_data()
    if not request_data:
        return

    body = json.loads(request_data)
    component_id = body.get("outputs").get("id")
    if not isinstance(component_id, dict):
        return
    component_type = component_id.get("type")

    if not component_type == LacyContainer.ids.container("none").get("type"):
        return
    
    node_id = UUID(component_id.get("index"))
    inputs = body.get("inputs", [])
    state = body.get("state", [])
    args = inputs_to_vals(inputs + state)
    _, variables, pathname_, search_, loading_state_ = args
    query_parameters = _parse_query_string(search_)
    node_variables = json.loads(variables)
    
    lacy_node: PageNode = router.route_table.get(node_id)
    path = router.strip_relative_path(pathname_)
    segments = path.split('/')
    node_segments = [segment.strip('()') for segment in lacy_node.module.split('.')[1:-1]]
    current_index = node_segments.index(lacy_node.segment)
    remaining_segments = segments[current_index: ]

    exec_tree, endpoints = router.build_execution_tree(
        current_node=lacy_node,
        segments=remaining_segments,
        parent_variables=node_variables,
        query_params=query_parameters,
        loading_state=loading_state_,
        request_pathname=path,
        endpoints={},
        is_init=False,
    )

    endpoint_results = await router.gather_endpoints(endpoints)
    layout = await exec_tree.execute(is_init=False, endpoints=endpoint_results)
    return layout


if __name__ == "__main__":
    app.run(debug=False, port=8031)
