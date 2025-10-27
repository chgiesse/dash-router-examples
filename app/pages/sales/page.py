import dash_mantine_components as dmc
from dash_router import ChildContainer, RouteConfig
from global_components.tabs import PageTabs


config = RouteConfig(default_child="overview")


async def layout(children: ChildContainer, **kwargs):
    tab = children.props.active
    tabs = [
        {"label": "Overview", "href": "/sales/overview"},
        {"label": "Invoices", "href": "/sales/invoices"},
        {"label": "Dashboard", "href": "/sales/dashboard"},
        {"label": "Plotly", "href": "/sales/analytics"},
    ]

    return dmc.Stack(
        [
            PageTabs(tabs, tab),
            dmc.Box(
                children,
                mx="auto", # type: ignore
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
            ),
        ],
    )
