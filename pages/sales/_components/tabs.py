import dash_mantine_components as dmc
from dash_iconify import DashIconify


class SalesTabs(dmc.Tabs):

    class ids:
        tabs = "sales-tabs"

    def __init__(self, active_tab: str = None, **kwargs):
        super().__init__(
            id=self.ids.tabs,
            variant="pills",
            value=active_tab,
            radius="xl",
            children=dmc.TabsList(
                [
                    dmc.Anchor(
                        dmc.TabsTab(
                            "Overview",
                            value="overview",
                            leftSection=DashIconify(
                                icon="radix-icons:dot", height=20
                            ).to_plotly_json(),
                            py=8,
                        ),
                        href="/sales/overview",
                        underline=False,
                    ),
                    dmc.Anchor(
                        dmc.TabsTab(
                            "Invoices",
                            value="invoices",
                            py=8,
                            leftSection=DashIconify(
                                icon="radix-icons:dot", height=20
                            ).to_plotly_json(),
                        ),
                        href="/sales/invoices",
                        underline=False,
                    ),
                    dmc.Anchor(
                        dmc.TabsTab(
                            "Dashboard",
                            value="dashboard",
                            py=8,
                            leftSection=DashIconify(
                                icon="radix-icons:dot", height=20
                            ).to_plotly_json(),
                        ),
                        href="/sales/dashboard",
                        underline=False,
                    ),
                    dmc.Anchor(
                        dmc.TabsTab(
                            "Plotly",
                            value="analytics",
                            py=8,
                            leftSection=DashIconify(
                                icon="radix-icons:dot", height=20
                            ).to_plotly_json(),
                        ),
                        href="/sales/analytics",
                        underline=False,
                    ),
                    # dmc.Anchor(dmc.TabsTab('Invoices', value='invoices'), href='/sales/invoices', underline=False),
                ]
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
