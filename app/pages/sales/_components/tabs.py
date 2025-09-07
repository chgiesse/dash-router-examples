import dash_mantine_components as dmc
from dash_iconify import DashIconify


class SalesTabs(dmc.Tabs):

    class ids:
        tabs = "sales-tabs"

    def __init__(self, active_tab: str = None, **kwargs):
        super().__init__(
            id=self.ids.tabs,
            value=active_tab,
            children=dmc.TabsList(
            [
                dmc.Anchor(
                dmc.TabsTab(
                    "Overview",
                    value="overview",
                    className="mainLink",
                ),
                href="/sales/overview",
                underline=False,
                ml={"xxl": "12.5%", "xl": "7.5%", "lg": "7.5%", "md": "7.5%", "sm": "5%", "xs": "2.5%", "xxs": "2.5%"},
                ),
                dmc.Anchor(
                dmc.TabsTab(
                    "Invoices",
                    value="invoices",
                    className="mainLink",
                ),
                href="/sales/invoices",
                underline=False,
                ),
                dmc.Anchor(
                dmc.TabsTab(
                    "Dashboard",
                    value="dashboard",
                    className="mainLink",
                ),
                href="/sales/dashboard",
                underline=False,
                ),
                dmc.Anchor(
                dmc.TabsTab(
                    "Plotly",
                    value="analytics",
                    className="mainLink",
                ),
                href="/sales/analytics",
                underline=False,
                ),
            ],
            grow=True,
            justify="flex-start",
            ),
        )


class Tabs(dmc.Paper):

    def __init__(self, active: str):

        create_navlink = lambda href, icon, label, active: dmc.NavLink(
            label=label,
            href=href,
            active="partial",
            variant="filled",
            leftSection=DashIconify(icon=icon, height=20).to_plotly_json(),
            fw=700,
            w="fit-content",
            h=35,
            # **{'data-active': True} if label.lower() == active else {}
        )

        super().__init__(
            radius="xl",
            withBorder=True,
            p=5,
            shadow="md",
            w="32rem",
            children=dmc.Group(
                [
                    create_navlink(
                        label="Overview",
                        href="/sales/overview",
                        icon="material-symbols:calendar-view-week",
                        active=active,
                    ),
                    create_navlink(
                        label="Invoices",
                        href="/sales/invoices",
                        icon="material-symbols:calendar-view-week",
                        active=active,
                    ),
                    create_navlink(
                        label="Analytics",
                        href="/sales/analytics",
                        icon="material-symbols:data-usage-rounded",
                        active=active,
                    ),
                ],
                justify="space-between",
                gap="xs",
                grow=True,
            ),
        )
