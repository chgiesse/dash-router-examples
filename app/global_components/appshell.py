import dash_mantine_components as dmc

from global_components.sidebar import navbar
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


def create_appshell(content):
    return dmc.MantineProvider(
        forceColorScheme="dark",
        theme={
            "primaryColor": "violet",
            "primareShade": "3",
            "defaultRadius": "md",
            "components": {"Card": {"defaultProps": {"shadow": "sm"}}},
            "focusRing": "never",
            "colors": {
                "dark": mantine_dark,
                "slate": list(reversed(shadcn_slate)),
            },
        },
        children=dmc.AppShell(
            [
                navbar,
                NotificationsContainer(),
                Url(),
                dmc.AppShellMain(
                    content,
                ),
            ],
            padding="md",
            navbar={
                "width": 65,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
        ),
    )
