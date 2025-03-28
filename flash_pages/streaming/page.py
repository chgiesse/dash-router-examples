import dash_mantine_components as dmc 
from dash_iconify import DashIconify
from dash_router import ChildContainer, RouteConfig

config = RouteConfig(default_child='live-dashboard')

async def layout(children: ChildContainer, **kwargs):

    create_navlink = lambda href, icon, label: dmc.NavLink(
            label=label,
            href=href,
            active="partial",
            variant='filled',
            leftSection=DashIconify(icon=icon, height=20).to_plotly_json(),
            fw=700,
            w='fit-content',
            h=35,
        )

    return dmc.Stack(
        children=[
            dmc.Paper(
            radius='xl',
            withBorder=True,
            p=5,
            shadow='md',
            w='fit-content',
            children=dmc.Group(
                [
                    create_navlink(
                        label="Live Dashboard",
                        href="/streaming/live-dashboard",
                        icon='material-symbols:campaign-outline-rounded',
                    ),
                    create_navlink(
                        label="Components",
                        href="/streaming/live-components",
                        icon='material-symbols:encrypted-outline-rounded',
                    )
                ], 
                justify='center', 
                gap='xs'
                )
            ),
            children
        ]
    )