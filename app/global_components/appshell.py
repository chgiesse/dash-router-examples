import dash_mantine_components as dmc
from dash import dcc

from global_components.sidebar import navbar, theme_toggle
from global_components.header import header
from global_components.notifications import NotificationsContainer
from global_components.location import Url

shadcn_gray = [
    "#030712",
    "#111827",
    "#1f2937",
    "#374151",
    "#4b5563",
    "#6b7280",
    "#9ca3af",
    "#e5e7eb",
    "#f3f4f6",
    "#f9fafb",
]

shadcn_slate = [
    "#020617",
    "#0f172a",
    "#1e293b",
    "#334155",
    "#475569",
    "#64748b",
    "#94a3b8",
    "#e2e8f0",
    "#f1f5f9",
    "#f8fafc",
]

mantine_dark = [
    "#d3d4d6",
    "#7a7e83",
    "#383e46",
    "#4a5d79",
    "#222831",
    "#1f242c",
    "#181c22",
    "#0e1014",
    "#14181d",
    "#1b2027",
]

blue = [
    "#ecf4ff",
    "#dce4f5",
    "#b9c7e2",
    "#94a8d0",
    "#748dc0",
    "#5f7cb7",
    "#5474b4",
    "#44639f",
    "#3a5890",
    "#2c4b80",
]


def create_appshell(content):
    return dmc.MantineProvider(
        defaultColorScheme="auto",
        theme={
            "primaryColor": "blue",
            "primareShade": "6",
            "defaultRadius": "md",
            "components": {"Card": {"defaultProps": {"shadow": "sm"}}},
            "focusRing": "never",
            "colors": {
                # "dark": list(reversed(shadcn_slate)),
                "dark": list(reversed(shadcn_gray)),
                "slate": list(reversed(shadcn_slate)),
                "shadc_gray": list(reversed(shadcn_gray)),
                "blue": blue
            },
        },
        children=dmc.AppShell(
            [
                # Persistent store for theme or other global preferences
                # dcc.Store(id="color-scheme-store", storage_type="local"),
                # navbar,
                # theme_toggle,
                NotificationsContainer(),
                Url(),
                header,
                dmc.AppShellMain(
                    content
                ),
            ],
            # padding="md",
            header={
                "height": 55,
            }
            # navbar={
            #     "width": 65,
            #     "breakpoint": "sm",
            #     "collapsed": {"mobile": True},
            # },
        ),
    )
