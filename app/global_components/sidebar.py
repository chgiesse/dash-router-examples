import dash_mantine_components as dmc
from dash.html import Div
from dash_iconify import DashIconify
# from flash import Input, Output, clientside_callback
from dash import Input, Output, clientside_callback

from utils.helpers import get_icon

theme_toggle = dmc.Switch(
    offLabel=DashIconify(
        icon="line-md:sun-rising-loop",
        width=15,
        color=dmc.DEFAULT_THEME["colors"]["yellow"][8],
    ),
    onLabel=DashIconify(
        icon="line-md:moon-rising-alt-loop",
        width=15,
        color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
    ),
    id="color-scheme-toggle",
    persistence=True,
    color="gray",
)


def create_navlink(href: str, icon: str, *args, **kwargs):
    return dmc.Anchor(
        dmc.ActionIcon(get_icon(icon, height=25), size="xl", variant="subtle"),
        href=href,
        *args,
        **kwargs,
    )


navbar = dmc.AppShellNavbar(
    [
        dmc.Stack(
            align="center",
            gap="sm",
            mt="lg",
            pb="lg",
            style={"marginBottom": "auto"},
            children=[
                get_icon("mingcute:flash-circle-line", height=35),
                create_navlink(
                    href="/",
                    icon="material-symbols:home-outline-rounded",
                ),
                create_navlink(href="/sales", icon="icon-park-outline:sales-report"),
                create_navlink(href="/files/1/2/3/4", icon="majesticons:file-line"),
                create_navlink(
                    href="/nested-route",
                    icon="material-symbols:route-outline",
                ),
                create_navlink(
                    href="/streaming/live-dashboard",
                    icon="material-symbols:stream-rounded",
                ),
            ],
        ),
        dmc.Box(theme_toggle, my="md", mx="auto"),
    ],
)
