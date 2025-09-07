from utils.helpers import get_icon
from global_components.theme import ThemeComponent
import dash_mantine_components as dmc
from flash import clientside_callback, Input, Output, ALL, State
from flash_router import RootContainer
from dash import html
from dash_iconify import DashIconify

# ---------------------------------------------------------------------------
# Centralized configuration dictionaries for search modal items
# ---------------------------------------------------------------------------
# Ordered dicts (regular dict preserves insertion order in Python 3.7+)
ROUTER_LINKS = {
    # prefix: metadata
    "pages": {
        "title": "Pages & App Structure",
        "description": "Create multi-page apps with nested layouts via your filesystem",
        "icon": "tabler:list-tree",
        "href": "/sales/invoices?page=1",
    },
    "data_fetching": {
        "title": "Data Fetching",
        "description": "Assign data to layouts for absolute parallelism",
        "icon": "tdesign:tree-round-dot",
        "href": "/sales/analytics",
    },
    "parallel_router": {
        "title": "Parallel Routes",
        "description": "Define Sub-Routes and Child-Routes that render in parallel",
        "icon": "si:flow-parallel-duotone",
        "href": "/sales/invoices/3/positions?page=1",
    },
    "smart_query_params": {
        "title": "Smart Query Params",
        "description": "Use layout inputs as query params with Pydantic models and validation",
        "icon": "codicon:symbol-parameter",
        "href": "/streaming/live-dashboard",
    },
}

SEARCH_LINKS = {
    # prefix: metadata (keep href destinations intact)
    "event_callback": {
        "title": "Event Callback",
        "description": "Callback api for sse - progressive UI updates & endless streaming",
        "icon": "icon-park-outline:blocks-and-arrows",
        "href": "/nested-route/child-1",
    },
    "sse": {
        "title": "Server Sent Events",
        "description": "Create server sent events endpoints",
        "icon": "tabler:arrows-join",
        "href": "/nested-route/child-2",
    },
    "websocket": {
        "title": "Websockets",
        "description": "Hook into Quart Websockets",
        "icon": "line-md:arrows-vertical-alt",
        "href": "/nested-route/child-3",
    },
}

header_links = [
    {"label": "Docs", "href": "/sales"},
    {"label": "Showcase", "href": "/nested-route"},
    {"label": "Tips & Tricks", "href": "/streaming/live-dashboard"},
    {"label": "Integrations", "href": "#"},
    {"label": "Blog", "href": "#"},
]

def nav_anchor(label, href):
    return dmc.Anchor(label, href=href, className="mainHeaderLink", unstyled=True, p=0)

class MobileDrawer(dmc.Box):

    class ids:
        drawer = "mobile-drawer"
        burger = "navbar-burger"

    clientside_callback(
        """
        //js
        function (burgerOpened, drawerOpened) {
            const triggered = window.dash_clientside.callback_context.triggered_id;
            if (triggered === undefined) {
                return window.dash_clientside.no_update;
            }

            if (triggered === 'navbar-burger') {
                return [burgerOpened, window.dash_clientside.no_update];
            }

            if (triggered === 'mobile-drawer') {
                if (drawerOpened === false) {
                    return [window.dash_clientside.no_update, false];
                }
                return window.dash_clientside.no_update;
            }

            return window.dash_clientside.no_update;
        }
        ;//
        """,
        [Output(ids.drawer, "opened"), Output(ids.burger, "opened", allow_duplicate=True)],
        Input(ids.burger, "opened"),
        Input(ids.drawer, "opened"),
        prevent_initial_call=True,
    )

    clientside_callback(
        "( pathChange ) => { console.log(pathChange); return false }",
        Output(ids.drawer, "opened", allow_duplicate=True),
        Input(RootContainer.ids.location, "pathname"),
        prevent_initial_call=True,
    )

    def __init__(self):
        drawer_items = []
        for item in header_links:
            drawer_items.append(
                dmc.Anchor(
                    dmc.Paper(
                        dmc.Group(
                            [
                                dmc.Text(item['label'], fw='bold'),
                                DashIconify(icon='material-symbols:chevron-right-rounded', height=18),
                            ],
                            justify='space-between',
                        ),
                        p='sm',
                        withBorder=True,
                    ),
                    href=item['href'],
                    underline='never',
                    w='100%'
                )
            )

        drawer = dmc.Drawer(
            id=self.ids.drawer,
            padding="md",
            position="bottom",
            withCloseButton=True,
            closeOnClickOutside=True,
            children=dmc.Stack(
                children=drawer_items,
                gap="md",
            ),
        )

        burger = dmc.ActionIcon(
            dmc.Burger(
                id="navbar-burger",
                opened=False,
                size="sm",
            ),
            size="lg",
            color="dark",
            variant="default",
            className="main-button",
            h=36
        )

        super().__init__(
            [drawer, burger],
            display={"xxs": "flex", "xs": "flex", "sm": "none", "md": "none", "lg": "none", "xl": "none"},
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

        # Build children dynamically from config dicts
        search_children = [
            dmc.TextInput(
                id=self.ids.search_input,
                variant="unstyled",
                w="100%",
                leftSection=DashIconify(
                    icon="material-symbols:search-rounded", height=25
                ),
                size="md",
                placeholder="Search nested route...",
            ),
            dmc.Divider(label="Router", className="links-divider"),
        ]
        # Add links divider and linked pages
        # search_children.append(
        #     dmc.Divider(label="Router", className="links-divider")
        # )

        # Add filter buttons
        for prefix, meta in ROUTER_LINKS.items():
            search_children.append(
                create_search_link(
                    meta["title"],
                    meta["description"],
                    meta["icon"],
                    prefix,
                    meta["href"],
                )
            )

        # Add links divider and linked pages
        search_children.append(
            dmc.Divider(label="Streams", className="links-divider")
        )
        for prefix, meta in SEARCH_LINKS.items():
            search_children.append(
                create_search_link(
                    meta["title"],
                    meta["description"],
                    meta["icon"],
                    prefix,
                    meta["href"],
                )
            )

        modal_content = dmc.Stack(
            align="stretch",
            gap="xs",
            children=search_children,
        )

        super().__init__(
            id=self.ids.modal,
            withCloseButton=False,
            overlayProps={
                "backgroundOpacity": 0.55,
                "blur": 3,
            },
            size="45rem",
            transitionProps={"transition": "pop"},
            children=modal_content,
        )

class ids:
    search_button = "search-input-trigger"
    search_icon_button = "search-icon-trigger"

clientside_callback(
    """
    //js
    function ( nClicksInput, nClicksIcon, opened ) {
        // If neither has been clicked yet, do nothing
        if ((nClicksInput || 0) + (nClicksIcon || 0) === 0) {
            return
        }
        // Toggle modal state
        return !opened
    }
    ;//
    """,
    Output(SearchModal.ids.modal, "opened"),
    Input(ids.search_button, "n_clicks"),
    Input(ids.search_icon_button, "n_clicks"),
    State(SearchModal.ids.modal, "opened"),
)

logo = dmc.Anchor(
    dmc.Group(
        align="center",
        justify="center",
        gap=5,
        mb=6,
        children=[
            get_icon("mingcute:flash-circle-line", height=35),
            dmc.Title(
                "Flash",
                order=2,
                className="sansation-bold sansation-regular-italic logo-title italic-adjust",
                style={
                    "fontFamily": "Sansation, sans-serif",
                    "fontWeight": 700,
                    "fontStyle": "italic",
                    "color": "inherit",
                    "textDecoration": "none",
                    "lineHeight": 1,
                },
            ),
        ],
        # className="logo-wrap",
    ),
    unstyled=True,
    underline="never",
    href="/",
    style={"textDecoration": "none", "color": "inherit"},
    mr="xs"
)

version_badge = dmc.Anchor(
    [
        dmc.Badge(
            "v1.2.1",
            variant="outline",
            size="lg",
            radius="md",
            h=35,
            leftSection=get_icon("mingcute:tag-line"),
            color="dark",
            darkHidden=True,
        ),
        dmc.Badge(
            "v1.2.1",
            variant="outline",
            size="lg",
            radius="md",
            h=35,
            leftSection=get_icon("mingcute:tag-line"),
            lightHidden=True,
        ),
    ],
    unstyled=True,
    href="https://pypi.org/project/dash-flash/",
    target="_blank",
    className="search-input-trigger",
    style={"textDecoration": "none", "color": "inherit"},
    p=0,
    display={"xxs": "none", "xs": "none", "sm": "none", "md": "flex", "lg": "flex", "xl": "flex"},
)

search_input = dmc.Box(
    html.Div(
        className="search-input-trigger",
        id=ids.search_button,
        style={"cursor": "pointer"},
        children=dmc.TextInput(
            className="search-input-trigger",
            variant="default",
            placeholder="Search",
            w=250,
            radius="md",
            leftSection=DashIconify(
                icon="material-symbols:input-circle-rounded",
                height=20,
                rotate=1,
            ),
            readOnly=True,
            rightSection=DashIconify(
                icon="material-symbols:search-rounded", height=20
            ),
        ),
    ),
    display={"xxs": "none", "xs": "none", "sm": "none", "md": "none", "lg": "flex", "xl": "flex"},
)

search_button = dmc.ActionIcon(
    DashIconify(
        icon="material-symbols:search-rounded",
        height=25,
        rotate=1,
    ),
    size="lg",
    className="main-button",
    color="dark",
    variant="default",
    display={"xxs": "flex", "xs": "flex", "sm": "flex", "md": "flex", "lg": "none", "xl": "none"},
    id=ids.search_icon_button,
    h=36
)

github_button = dmc.Anchor(
    dmc.ActionIcon(
        get_icon("line-md:github", height=25),
        size="lg",
        className="main-button",
        color="dark",
        variant="default",
        h=36
    ),
    unstyled=True,
    href="https://github.com/chgiesse/flash",
    target="_blank",
)

# github_button = dmc.ActionIcon(
#     get_icon("line-md:github", height=25),
#     size="lg",
#     className="main-button",
#     variant="default",
#     h=36,
# )

# theme_button = dmc.ActionIcon(
#     [
#         dmc.Box(
#             get_icon("line-md:moon-to-sunny-outline-transition", height=25),
#             darkHidden=True,
#         ),
#         dmc.Box(
#             get_icon("line-md:moon-twotone", height=25),
#             lightHidden=True,
#         ),
#     ],
#     size="lg",
#     color="dark",
#     variant="default",
#     id="color-scheme-toggle",
#     className="main-button",
#     h=36
# )

header_links_component = dmc.Group(
    [nav_anchor(item["label"], item["href"]) for item in header_links],
    gap="sm",
    display={"xxs": "none", "xs": "none", "sm": "flex", "md": "flex", "lg": "flex", "xl": "flex"},
)

header = dmc.AppShellHeader(
    withBorder=False,
    children=dmc.Group(
        align="center",
        justify="flex-start",
        mx="auto",
        w={"xxl": "75%", "xl": "85%", "lg": "85%", "md": "85%", "sm": "90%", "xs": "95%", "xxs": "95%"},
        gap="sm",
        h=55,
        children=[
            logo,
            header_links_component,
            dmc.Group(
                style={"marginLeft": "auto"},
                gap="sm",
                align="center",
                my="auto",
                children=[
                    SearchModal(),
                    version_badge,
                    search_input,
                    search_button,
                    github_button,
                    ThemeComponent(),
                    MobileDrawer()
                ],
            ),
        ],
    ),
)
