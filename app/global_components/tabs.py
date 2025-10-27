from typing import List, Dict
import dash_mantine_components as dmc

class PageTabs(dmc.Tabs):

    class ids:
        tabs = "sales-tabs"

    def __init__(self, tabs: List[Dict[str, str]], active_tab: str | None = None, **kwargs):

        create_navlink = lambda href, label, i: dmc.Anchor(
            dmc.TabsTab(
                label,
                value=href,
                className="mainLink",
            ),
            href=href,
            underline="never",
            **{"ml": {
                "xxl": "12.5%",
                "xl": "7.5%",
                "lg": "7.5%",
                "md": "7.5%",
                "sm": "5%",
                "xs": "2.5%",
                "xxs": "2.5%"
            }} if i == 0 else {}, # type: ignore
        )
        super().__init__(
            id=self.ids.tabs,
            value=active_tab,
            children=dmc.TabsList(
                [create_navlink(tab['href'], tab['label'], i) for i, tab in enumerate(tabs)],
                grow=True,
                justify="flex-start",
            ),
        )
