import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash_router import ChildContainer, RouteConfig
from global_components.tabs import PageTabs

config = RouteConfig(default_child="live-dashboard")


async def layout(children: ChildContainer, **kwargs):
    return [
        PageTabs(
            [
                {"label": "Dashboard", "href": "/streaming/live-dashboard"},
                {"label": "Components", "href": "/streaming/live-components"},
                {"label": "Feed", "href": "/streaming/feed-component"},
            ],
            children.props.active,
        ),
        dmc.Box(
            children,
            w={
                "xxl": "75%",
                "xl": "85%",
                "lg": "85%",
                "md": "85%",
                "sm": "90%",
                "xs": "99%",
                "xxs": "99%"
            }, # type: ignore
            px={
                "xxl": 0,
                "xl": 0,
                "lg": 0,
                "md": 0,
                "sm": "md",
                "xs": "sm",
                "xxs": "xs"
            }, # type: ignore
            mx="auto", # type: ignore
            mt="md"
        )
    ]
