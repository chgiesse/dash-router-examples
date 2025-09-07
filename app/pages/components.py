from flash import callback, Input, Output, State, no_update, MATCH
from dash import html
import dash_mantine_components as dmc
from dash_extensions import Lottie, EventListener
from typing import Literal


# Consistent height across feature cards for a clean grid
CARD_HEIGHT = "calc(32rem + var(--mantine-spacing-md))"


hero_section = dmc.Group(
    className='landing-page-content',
    mt="xl",
    children=[
        html.Div(
            className="hero-cta-glass hero-glass fade-in-bottom",
            children=[
                html.Ul(className="hero-features hero-features-cta", children=[
                    html.Li("Async-first"),
                    html.Li("Native streaming"),
                    html.Li("Advanced routing"),
                ]),
                html.Div(
                    className="cli-line",
                    children=[
                        html.Span("▲", className="cli-caret"),
                        html.Span(" ~ "),
                        html.Code("pip install dash-flash", className="cli-code"),
                    ],
                ),
            ],
        ),
    ],
)

hero_header = dmc.Center(
    className='landing-page-header',
    children=[
        html.Div(
            className="hero-panel",
            children=[
                dmc.Container(
                    dmc.Stack(
                        [
                            dmc.Title(
                                "The Async Python Framework for Full Stack Data Apps",
                                order=1,
                                className="hero-title",
                            ),
                            dmc.Text(
                                [
                                    "Flash helps you build ",
                                    html.Span("high‑quality, production-ready data applications", className="hero-em"),
                                    " with async execution, native streaming, and advanced routing.",
                                ],
                                size="lg",
                                style={"color": "var(--mantine-color-dimmed)"},
                                className="hero-subtitle",
                            ),
                            dmc.Text(
                                "Built on Dash Quart and Pydantic.",
                                size="sm",
                                style={"color": "var(--mantine-color-dimmed)"},
                                className="hero-subtagline",
                            ),
                        ],
                        gap="sm",
                        align="center",
                        className="fade-in"
                    ),
                    fluid=True,
                    px="md",
                ),
            ],
        ),
    ],
)

class LottieAnimation(EventListener):
    class ids:
        lottie_id = lambda idx: {"type": "lp-lotti-animation", "index": idx}
        listener_id = lambda idx: {"type": "lp-lotti-listener", "index": idx}

    @callback(
        Output(ids.lottie_id(MATCH), "action"),
        Input(ids.listener_id(MATCH), "n_events"),
        State(ids.listener_id(MATCH), "event"),
        prevent_initial_call=True,
    )
    def on_event(n_events, event):
        evet_type = event["type"] if event else None
        if n_events and evet_type == "mouseleave":
            return "stop"

        if n_events and evet_type == "mouseenter":
            return "play"

        return no_update


    def __init__(
        self,
        type: Literal["router", "stream"],
        lottie_url: str | None = None,
        w: int | str | float | None = None,
        loop: bool | int | float | None = None,
        h: int | str | float | None = None,
        children=None,
    ):
        """Create an EventListener that wraps arbitrary children.

        If `children` is provided, it's used as the wrapped content (so the
        listener covers the whole card). Otherwise a centered Lottie is
        rendered using `lottie_url` and sizing from `w`/`h`.
        """
        # If sizing not provided, let child components determine sizing
        h = w if h is None else h

        # Build the inner content: prefer explicit children, else construct a Lottie
        if children is not None:
            inner = children
        else:
            inner = dmc.Flex(
                Lottie(
                    options={
                        "loop": loop,
                        "autoplay": False,
                        "rendererSettings": {
                            "preserveAspectRatio": "xMidYMid slice"
                        },
                        "className": "lottie-animation",
                    },
                    url=lottie_url,
                    speed=0.5,
                    id=self.ids.lottie_id(type),
                ),
                h=h, w=w, align="center", justify="center"
            )

        super().__init__(
            inner,
            id=self.ids.listener_id(type),
            events=[
                {"event": "mouseenter", "props": ["type"]},
                {"event": "mouseleave", "props": ["type"]},
            ],
        )

router_card = LottieAnimation(
    "router",
    children=dmc.Card(
        # h=CARD_HEIGHT,
        withBorder=True,
        className="card-glass",
        children=[
            dmc.CardSection(
                # keep the lottie inside as a visual, but the listener now wraps the whole card
                dmc.Flex(
                    Lottie(
                        options={
                            "loop": 0,
                            "autoplay": False,
                            "rendererSettings": {"preserveAspectRatio": "xMidYMid slice"},
                            "className": "lottie-animation",
                        },
                        url="/assets/lottie/Router128.json",
                        speed=0.5,
                        id=LottieAnimation.ids.lottie_id("router"),
                    ),
                    h=200, w=256, align="center", justify="center"
                ),
                # withBorder=True,
                display="flex",
                style={
                    "justifyContent": "center",
                    "alignItems": "center"
                }
            ),
            dmc.Text("Flash Router", fw="bold", size="xl", mt="md"),
            dmc.List(
                [
                    dmc.ListItem("Filesystem‑based routing"),
                    dmc.ListItem("Parallel routes & sub‑rendering"),
                    dmc.ListItem("Smart query params"),
                    dmc.ListItem("Lazy loading"),
                ],
                m="md",
                spacing="sm",
                style={"fontSize": "1rem", "lineHeight": 1.55},
            ),
        ],
    ),
)

streamin_card = LottieAnimation(
    "stream",
    children=dmc.Card(
        # h=CARD_HEIGHT,
        # withBorder=True,
        className="card-glass",
        my="auto",
        children=[
            dmc.CardSection(
                dmc.Flex(
                    Lottie(
                        options={
                            "loop": 1,
                            "autoplay": False,
                            "rendererSettings": {"preserveAspectRatio": "xMidYMid slice"},
                            "className": "lottie-animation",
                        },
                        url="/assets/lottie/DynamicCubeLine(3).json",
                        speed=0.5,
                        id=LottieAnimation.ids.lottie_id("stream"),
                    ),
                    w=256 * 0.75, align="center", justify="center"
                ),
                display="flex",
                style={
                    "justifyContent": "center",
                    "alignItems": "center"
                }
            ),
            dmc.CardSection([
                dmc.Text("Streaming", fw="bold", size="xl", mb="md"),
                dmc.List(
                    [
                        dmc.ListItem("Real‑time dashboards, monitoring, push notifications, and progressive UI updates"),
                        dmc.ListItem("WebSockets & server‑sent events via Quart"),
                    ],
                    m="md",
                    spacing="sm",
                    style={"fontSize": "1rem", "lineHeight": 1.55},
                )
            ], p="md"),
        ],
    ),
)

callback_card = dmc.Card(
    withBorder=True,
    className="card-glass",
    p="md",
    h="16rem",
    children=[
        dmc.Text("Async‑first", fw="bold", size="xl", mb="xs"),
        dmc.Text(
            "Non‑blocking callbacks with Python async/await for snappy UIs.",
            style={"color": "var(--mantine-color-dimmed)"},
            size="sm",
            mb="xs",
        ),
        dmc.List(
            [
                dmc.ListItem("Concurrent background tasks"),
                dmc.ListItem("Seamless I/O without blocking"),
                dmc.ListItem("Predictable performance under load"),
            ],
            spacing="xs",
            style={"fontSize": "0.95rem", "lineHeight": 1.5},
        ),
    ],
)

layout_card = dmc.Card(
    withBorder=True,
    className="card-glass",
    p="md",
    h="16rem",
    children=[
        dmc.Text("Advanced routing", fw="bold", size="xl", mb="xs"),
        dmc.Text(
            "Compose complex apps with small, reusable pages.",
            style={"color": "var(--mantine-color-dimmed)"},
            size="sm",
            mb="xs",
        ),
        dmc.List(
            [
                dmc.ListItem("Nested routes & sub‑rendering"),
                dmc.ListItem("Smart query params"),
                dmc.ListItem("Lazy loading for fast startup"),
            ],
            spacing="xs",
            style={"fontSize": "0.95rem", "lineHeight": 1.5},
        ),
    ],
)

hero_content = dmc.Grid(
    maw=1100,
    grow=True,
    mx="xl",
    children=[
        dmc.GridCol(
            streamin_card,
            span={"xl": 4, "lg": 4, "md": 6, "sm": 6, "xs": 12},
            order={"xl": 1, "lg": 1, "md": 2, "sm": 2, "xs": 2},
            # maw=350,
            mx="auto",
        ),
        dmc.GridCol(
            dmc.Grid(
                [
                    dmc.GridCol(
                        callback_card,
                        span={"xxl": 12, "xl": 12, "lg": 12, "md": 6, "sm": 6, "xs": 12, "xxs": 12}
                    ),
                    dmc.GridCol(
                        layout_card,
                        span={"xxl": 12, "xl": 12, "lg": 12, "md": 6, "sm": 6, "xs": 12, "xxs": 12}
                    ),
                ],
                grow=True,
            ),
            span={"xl": 4, "lg": 4, "md": 12, "sm": 12, "xs": 12},
            order={"xl": 2, "lg": 2, "md": 3, "sm": 3, "xs": 3},
            # maw=350,
        ),
        dmc.GridCol(
            router_card,
            # h=CARD_HEIGHT,
            span={"xl": 4, "lg": 4, "md": 6, "sm": 6, "xs": 12},
            order={"xl": 3, "lg": 3, "md": 1, "sm": 1, "xs": 1},
            # maw=350,
            mx="auto",
        )
    ],
    # w="60vw",
)
