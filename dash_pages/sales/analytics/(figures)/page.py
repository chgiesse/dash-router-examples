from dash import html
import dash_mantine_components as dmc


def layout(
    figure_1=None,
    figure_2=None,
    figure_3=None,
    figure_4=None,
    figure_5=None,
    **kwargs
):
    basic_container = lambda children: dmc.Box(
        children, h=450, p="md", className="fade-in-chart"
    )

    return html.Div(
        children=[
            dmc.SimpleGrid(
                cols=2,
                children=[
                    basic_container(figure_1),
                    basic_container(figure_3),
                    basic_container(figure_5),
                    basic_container(figure_4),
                ],
            ),
            basic_container(figure_2),
        ]
    )
