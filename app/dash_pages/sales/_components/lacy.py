import dash_mantine_components as dmc
from dash import dcc
from flash import html


class LacyTestComponent(html.Div):
    class ids:
        output = "output-container"
        store = "lacy-store"
        input = "lacy-button"
        dummy = "dummy-output"

    # lcc = clientside_callback(
    #     """
    #     function ( updateData ) {
    #         console.log(updateData)
    #         const componentId = updateData.component_id
    #         const children = updateData.children
    #         // return window.dash_component_api.ExternalWrapper(children, componentId)
    #         window.dash_clientside.set_props(componentId, {children})
    #     }
    #
    #     """,
    #     Input(ids.store, "data"),
    #     prevent_initial_call=True,
    # )
    #
    # @callback(
    #     Output(ids.store, "data"),
    #     Input(ids.input, "n_clicks"),
    #     prevent_initial_call=True,
    # )
    # def update_store(_):
    #     output = dmc.Stack(
    #         [
    #             dmc.Title("Test lacy output"),
    #             dmc.Text("Blablablalb"),
    #             dmc.Text("Blablablalb"),
    #         ]
    #     )
    #
    #     response = {
    #         "children": recursive_to_plotly_json(output),
    #         "component_id": LacyTestComponent.ids.output,
    #     }
    #     return response

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            children=[
                dcc.Store(id=self.ids.store),
                dmc.Button("Load Lacy", id=self.ids.input),
                dmc.Center(id=self.ids.output),
                dmc.Box(id=self.ids.dummy),
            ],
        )
