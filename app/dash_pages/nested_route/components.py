from flash import Input, clientside_callback, Output, State, ALL
from dash import html
from dash_router import RootContainer
import dash_mantine_components as dmc
from dash_iconify import DashIconify


class SlotWrapper(html.Div):

    class ids:
        root_container = "first-level-slots-container"

    def __init__(self, children, *args, **kwargs) -> None:
        super().__init__(
            children=html.Div(
                children,
                *args,
                **kwargs,
            ),
            className=self.ids.root_container,
        )


class SearchModal(dmc.Modal):

    class ids:
        search_input = "splotlight-search-input"
        modal = "test-search-modal"
        item_card = lambda index: {"index": index, "type": "search-card"}
        item_link = lambda index: {"index": index, "type": "search-link"}

    filter_items_csc = clientside_callback(
        """
        //js
        function filterSearchItems(value) {
            // Early return if value is null
            if (value === null) return;

            const searchItems = document.querySelectorAll('.search-card');
            const visibleCount = { link: 0, btn: 0 };

            const toggleDivider = (selector, isVisible) => {
                const divider = document.querySelector(selector);
                if (divider) {
                    divider.style.display = isVisible ? 'block' : 'none';
                }
            }

            searchItems.forEach(card => {
                const searchKey = card.getAttribute('data-search-key');
                const itemType = card.getAttribute('data-search-item-type');

                const isVisible = searchKey.startsWith(value);

                card.style.display = isVisible ? 'block' : 'none';

                if (isVisible && (itemType === 'link' || itemType === 'btn')) {
                    visibleCount[itemType]++;
                }
            });

            toggleDivider('.filter-divider', visibleCount.btn > 0);
            toggleDivider('.links-divider', visibleCount.link > 0);
        }
        ;//
        """,
        Input(ids.search_input, "value"),
        prevent_initial_call=True,
    )

    set_value_csc = clientside_callback(
        """
        //js
        ( click ) => {
            const triggeredID = window.dash_clientside.callback_context.triggered_id
            if ( triggeredID === undefined ) {
                return
            }

            const searchPrefix = triggeredID.index
            const textInput = document.getElementById('splotlight-search-input').focus()
            return searchPrefix + ':'
        }
        ;//
        """,
        Output(ids.search_input, "value", allow_duplicate=True),
        Input(ids.item_card(ALL), "n_clicks"),
        prevent_initial_call=True,
    )

    clean_input_csc = clientside_callback(
        """( opened ) => { return opened ? window.dash_clientside.no_update : null }""",
        Output(ids.search_input, "value"),
        Input(ids.modal, "opened"),
    )

    close_modal_csc = clientside_callback(
        """
        //js
        function ( clicks ) {
            const trigerredId = window.dash_clientside.callback_context.trigerredId
            if (trigerredId === undefined ) {
                return
            }
            return false
        }
        ;//
        """,
        Output(ids.modal, "opened", allow_duplicate=True),
        Input(ids.item_link(ALL), "n_clicks"),
        prevent_initial_call=True,
    )

    def __init__(self):

        def create_search_card(title, description, icon):
            return dmc.Paper(
                p="sm",
                withBorder=True,
                children=dmc.Group(
                    [
                        DashIconify(icon=icon, height=25),
                        dmc.Box(
                            [
                                dmc.Text(title, fw=600),
                                dmc.Text(description, c="dimmed", size="xs"),
                            ]
                        ),
                    ]
                ),
            )

        def create_search_filter(title, description, icon, prefix):
            attributes = {"data-search-key": prefix, "data-search-item-type": "btn"}

            return html.Div(
                id=self.ids.item_card(prefix),
                className="search-card",
                children=create_search_card(title, description, icon),
                **attributes,
            )

        def create_search_link(title, description, icon, prefix, href):
            attributes = {"data-search-key": prefix, "data-search-item-type": "link"}

            return html.Div(
                id=self.ids.item_link(prefix),
                className="search-card",
                children=dmc.Anchor(
                    create_search_card(title, description, icon),
                    href=href,
                    underline=False,
                ),
                **attributes,
            )

        modal_content = dmc.Stack(
            align="stretch",
            gap="xs",
            children=[
                dmc.TextInput(
                    id=self.ids.search_input,
                    variant="unstyled",
                    w="100%",
                    leftSection=DashIconify(
                        icon="material-symbols:search-rounded", height=25
                    ).to_plotly_json(),
                    size="md",
                    placeholder="Search nested route...",
                ),
                dmc.Divider(label="Search With Prefix", className="filter-divider"),
                create_search_filter(
                    "ReferenceNumber",
                    "Search with contract level RN",
                    "material-symbols:quick-reference-outline",
                    "rn",
                ),
                create_search_filter(
                    "FinanceApplicationKey",
                    "Search with application level appkey",
                    "material-symbols:deployed-code-outline",
                    "appkey",
                ),
                create_search_filter(
                    "CustomerID",
                    "Search customer with cid",
                    "material-symbols:deployed-code-account-outline-rounded",
                    "cid",
                ),
                dmc.Divider(label="Pages Overview", className="links-divider"),
                create_search_link(
                    "Campaign",
                    "Go to Campaign page",
                    "material-symbols:campaign-outline-rounded",
                    "campaign",
                    "/nested-route/child-1",
                ),
                create_search_link(
                    "Security",
                    "Go to Security page",
                    "material-symbols:encrypted-outline-rounded",
                    "security",
                    "/nested-route/child-2",
                ),
                create_search_link(
                    "Explore",
                    "Go to Explore page",
                    "material-symbols:explore-outline-rounded",
                    "explore",
                    "/nested-route/child-3",
                ),
            ],
        )

        super().__init__(
            id=self.ids.modal,
            withCloseButton=False,
            overlayProps={
                "backgroundOpacity": 0.55,
                "blur": 3,
            },
            size="45rem",
            transitionProps={"transition": "slide-down"},
            children=modal_content,
        )


class Tabs(dmc.Paper):

    class ids:
        search_button = "search-input-trigger"

    clientside_callback(
        """
        //js
        function ( nClicks, opened ) {
            if ( nClicks === undefined ) {
                return
            }
            const nextOpened = !opened
            return nextOpened
        }
        ;//
        """,
        Output(SearchModal.ids.modal, "opened"),
        Input(ids.search_button, "n_clicks"),
        State(SearchModal.ids.modal, "opened"),
    )

    def __init__(self):

        create_navlink = lambda href, icon, label: dmc.NavLink(
            label=label,
            href=href,
            active="partial",
            variant="filled",
            leftSection=DashIconify(icon=icon, height=20).to_plotly_json(),
            fw=700,
            w="fit-content",
            h=35,
        )

        super().__init__(
            radius="xl",
            withBorder=True,
            p=5,
            shadow="md",
            children=dmc.Group(
                [
                    # SearchModal(),
                    create_navlink(
                        label="Campaign",
                        href="/nested-route/child-1",
                        icon="material-symbols:campaign-outline-rounded",
                    ),
                    create_navlink(
                        label="Security",
                        href="/nested-route/child-2",
                        icon="material-symbols:encrypted-outline-rounded",
                    ),
                    create_navlink(
                        label="Explore",
                        href="/nested-route/child-3",
                        icon="material-symbols:explore-outline-rounded",
                    ),
                    html.Div(
                        id=self.ids.search_button,
                        children=dmc.TextInput(
                            placeholder="Search",
                            className="text-input-button",
                            w=250,
                            radius="xl",
                            h=35,
                            leftSection=DashIconify(
                                icon="material-symbols:input-circle-rounded",
                                height=20,
                                rotate=1,
                            ).to_plotly_json(),
                            variant="filled",
                            readOnly=True,
                            rightSection=DashIconify(
                                icon="material-symbols:search-rounded", height=20
                            ).to_plotly_json(),
                        ),
                    ),
                ],
                justify="space-between",
                gap="xs",
            ),
        )
