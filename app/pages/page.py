from global_components.theme import landing_background
from .components import hero_header, hero_section, hero_content

import dash_mantine_components as dmc
from dash_extensions import Lottie
from dash import html

layout = html.Div(
    children=[
        html.Div(
            children=[
                landing_background(total=16),
                dmc.ScrollArea(
                    dmc.Stack(
                        [
                            hero_header,
                            hero_section,
                            dmc.Space(h=50),
                            hero_content
                        ],
                        align="center",
                        gap="xl",
                        py="md",
                    ),
                    # className="bg-overlay-stack",
                    h="calc(100vh - var(--app-shell-header-height) - 20px)",
                    type="scroll"
                )
            ],
            className="landing-page-bg",
        )
    ],
)
