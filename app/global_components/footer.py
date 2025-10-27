"""
Footer component example - demonstrating reuse of header components with pattern matching.

This shows how the SearchBar class with pattern-matching IDs allows you to create multiple instances
of search components (input and button) by simply changing the location parameter.

The SearchModal and theme_store stay as single global instances (no pattern matching needed).
"""

from utils.helpers import get_icon
from global_components.theme import ThemeToggle
from global_components.header import (
    MobileDrawer,
    SearchModal,
    SearchBar,
    nav_anchor,
    header_links,
    logo
)
import dash_mantine_components as dmc
from dash import html


# Register the callback for footer search components to toggle the same SearchModal
SearchBar.register_modal_toggle_callback(location="footer", modal_id=SearchModal.ids.modal)

# Register the callback for footer theme button to toggle the same theme store
ThemeToggle.register_theme_callback(location="footer")

# Create footer-specific search components with "footer" location
footer_search_input = SearchBar.create_search_input("footer")
footer_search_button = SearchBar.create_search_button("footer",size="xl", icon_height=30)  # Example of customizing button height

# Create footer-specific theme button with "footer" location
footer_theme_button = ThemeToggle.create_button("footer", size="xl", icon_height=30)

footer_links_component = dmc.Group(
    [nav_anchor(item["label"], item["href"]) for item in header_links],
    gap="sm",
    display={
        "xxs": "none",
        "xs": "none",
        "sm": "flex",
        "md": "flex",
        "lg": "flex",
        "xl": "flex"
    }, # type: ignore
)

github_button = dmc.Anchor(
    dmc.ActionIcon(
        get_icon("line-md:github", height=30),
        size="xl",
        variant="transparent",
        h=36,
        c="light-dark(var(--mantine-color-dark-9), var(--mantine-color-white))",
    ),
    unstyled=True,
    href="https://github.com/chgiesse/flash",
    target="_blank",
)

# Example footer using the same components with "footer" location
footer = dmc.AppShellFooter(
    h=60,
    withBorder=True,
    hiddenFrom="xs",
    children=dmc.Group(
        align="center",
        justify="center",
        # display={"xxl": "none", "xl": "none", "lg": "none", "md": "none", "sm": "none", "xs": "none", "xxs": "95%"}, # type: ignore
        gap="xl",
        h=60,
        children=[
            footer_theme_button,  # Footer theme toggle button
            github_button,
            dmc.Anchor(
                get_icon("mingcute:flash-circle-line", height=45),
                unstyled=True,
                underline="never",
                href="/",
                c="light-dark(var(--mantine-color-dark-9), var(--mantine-color-white))",
            ),
            footer_search_button,
            MobileDrawer(location="footer", size="xl", bsize=30),  # MobileDrawer supports pattern matching
        ],
    ),
)
