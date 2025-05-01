import dash_mantine_components as dmc
from dash import html, Output, Input, State, ctx, callback, Dash, register_page, page_container, no_update
import time

min_step = 0
max_step = 3
active = 1

app = Dash(__name__, use_pages=True, pages_folder="")

def create_stepper(num, active):

    create_step = lambda n: dmc.StepperStep(
        label="First step",
        description="Create an account",
        children=dmc.Text(f"Step {n}", ta="center"),
    )

    return dmc.Stepper(
        id="stepper-basic-usage",
        active=active,
        children=[create_step(i) for i in range(num)],
    )


def stepper_layout(**kwargs):

    step = int(kwargs.get('step')) if kwargs.get('step') else 0
    reduce = step % 2 == 0
    num = 4 if not reduce else 2

    return dmc.Box(
        p='md',
        children=[
            create_stepper(num, step),
            dmc.Group(
                justify="center",
                mt="xl",
                children=[
                    dmc.Button("Back", id="back-basic-usage", variant="default"),
                    dmc.Button("Next step", id="next-basic-usage"),
                ],
            )
        ]
    )

register_page("home", path='/home', layout=stepper_layout)
app.layout = dmc.MantineProvider(page_container)


@callback(
    Output("_pages_location", "search"),
    Input("back-basic-usage", "n_clicks"),
    Input("next-basic-usage", "n_clicks"),
    State("stepper-basic-usage", "active"),
    prevent_initial_call=True,
)
def update(back, next_, current):
    button_id = ctx.triggered_id
    if not button_id:
        return no_update
    step = current if current is not None else active
    if button_id == "back-basic-usage":
        step = step - 1 if step > min_step else step
    else:
        step = step + 1 if step < max_step else step
    return f'?step={step}'


if __name__ == '__main__':
    app.run(port=8008, debug=True)
