import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash_router import ChildContainer, RouteConfig

config = RouteConfig(default_child="live-dashboard")


async def layout(children: ChildContainer, **kwargs):
    print("streaming layout", kwargs, flush=True)
    create_navlink = lambda href, icon, label: dmc.NavLink(
        label=label,
        href=href,
        active="exact",
        variant="filled",
        leftSection=DashIconify(icon=icon, height=20).to_plotly_json(),
        fw=700,
        w="fit-content",
        h=35,
    )

    return dmc.Stack(
        children=[
            dmc.Paper(
                radius="xl",
                withBorder=True,
                p=5,
                w="fit-content",
                mx="auto",
                children=dmc.Group(
                    [
                        create_navlink(
                            label="Live Dashboard",
                            href="/streaming/live-dashboard",
                            icon="fluent:stream-20-filled",
                        ),
                        create_navlink(
                            label="Components",
                            href="/streaming/live-components",
                            icon="lucide:component",
                        ),
                    ],
                    justify="center",
                    gap="xs",
                ),
            ),
            children,
        ],
        # align="center",
    )
