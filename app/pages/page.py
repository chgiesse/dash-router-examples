import dash_mantine_components as dmc
from dash import html
from global_components.theme import landing_background
from global_components.sidebar import get_icon
import random


async def layout(**kwargs):
    lines = landing_background(total=16)
    return html.Div(
        className="landing-page-bg",
        children=[
            lines,
            html.Div(
                className='landing-page-header',
                children=[
                    dmc.Container(
                        dmc.Stack(
                            [
                                dmc.Title(
                                    "The Async Python Framework for Data Apps",
                                    order=1,
                                    className="hero-title",
                                ),
                                dmc.Text(
                                    [
                                        "Flash helps you build ",
                                        html.Span("high‑quality, production-ready data applications", className="hero-em"),
                                        " with async execution, native streaming, and advanced routing.",
                                    ],
                                    size="lg",
                                    c="dimmed",
                                    className="hero-subtitle",
                                ),
                                dmc.Text(
                                    "Built on Dash Quart and Pydantic.",
                                    size="sm",
                                    c="dimmed",
                                    className="hero-subtagline",
                                ),
                            ],
                            gap="sm",
                            align="center",
                        ),
                        fluid=True,
                        px="md",
                    ),
                ],
            ),
            html.Div(
                className='landing-page-content',
                children=[
                    html.Div(
                        className="hero-cta-glass hero-glass",
                        children=[
                            html.Ul(className="hero-features hero-features-cta", children=[
                                html.Li("Async-first"),
                                html.Li("Native streaming"),
                                html.Li("Advanced routing"),
                            ]),
                            html.Div(
                                className="cli-line",
                                children=[
                                    html.Span("▲", className="cli-caret"),
                                    html.Span(" ~ "),
                                    html.Code("pip install dash-flash", className="cli-code"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
