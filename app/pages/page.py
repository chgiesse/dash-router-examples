from global_components.theme import landing_background
from .components import hero_header, hero_section, hero_content

import dash_mantine_components as dmc
from dash import html

layout = html.Div(
    children=[
        html.Div(
            children=[
                landing_background(total=16),
                html.Div(
                    dmc.Stack(
                        [
                            hero_header,
                            hero_section,
                            dmc.Group([
                                dmc.Button(
                                    "Get Started",
                                    size="md",
                                    variant="white",
                                    w="10.5rem",
                                    lightHidden=True
                                ),
                                dmc.Button(
                                    "Get Started",
                                    size="md",
                                    color="dark",
                                    w="10.5rem",
                                    darkHidden=True
                                ),
                                dmc.Button(
                                    "View on GitHub",
                                    size="md",
                                    variant="default",
                                    color="dark",
                                    className="main-button",
                                    w="10.5rem"
                                ),
                            ], my="xl"),
                            hero_content
                        ],
                        align="center",
                        gap="xl",
                        py="md",
                    ),
                    style={
                        "height": "calc(100dvh - var(--mantine-header-height, 60px))",
                        "overflowY": "auto",
                        "paddingLeft": "var(--mantine-spacing-xs)"
                    },
                )
            ],
            className="landing-page-bg",
        )
    ],
)
