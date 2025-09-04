from flash import callback, Input, Output, State, no_update, MATCH
from dash import html
import dash_mantine_components as dmc
from dash_extensions import Lottie, EventListener
from typing import Literal


# Consistent height across feature cards for a clean grid
CARD_HEIGHT = "calc(26rem + var(--mantine-spacing-md))"


hero_section = html.Div(
    className='landing-page-content',
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
        lottie_url: str,
        w: int | str | float,
        loop: bool | int | float | None = None,
        h: int | str | float | None = None,

    ):
        h = w if h is None else h
        super().__init__(
            dmc.Flex(
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
            ),
        id=self.ids.listener_id(type),
        events=[
            {"event": "mouseenter", "props": ["type"]},
            {"event": "mouseleave", "props": ["type"]},
        ],
    )


router_card = dmc.Card(
    h=CARD_HEIGHT,
    withBorder=True,
    className="card-glass",
    children=[
        dmc.CardSection(
            LottieAnimation(
                "router",
                lottie_url="/assets/lottie/Router128.json",
                h=200,
                loop=0,
                w=256 * 1.5,
            ),
            withBorder=True,
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
)

streamin_card = dmc.Card(
    h=CARD_HEIGHT,
    withBorder=True,
    className="card-glass",
    children=[
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
        ], p="md", withBorder=True),
        dmc.CardSection(
            LottieAnimation(
                "stream",
                lottie_url="/assets/lottie/DynamicCubeLine(3).json",
                w=256 * 0.75,
                loop=1
            ),
            withBorder=True,
            display="flex",
            style={
                "justifyContent": "center",
                "alignItems": "center"
            }
        ),
    ],
)


hero_content = dmc.SimpleGrid(
    mt="xl",
    cols=3,
    children=[
        streamin_card,
        dmc.Stack([
            dmc.Card(
                withBorder=True,
                className="card-glass",
                p="md",
                h="12.75rem",
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
            ),
            dmc.Card(
                withBorder=True,
                className="card-glass",
                p="md",
                h="12.75rem",
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
            ),
        ]),
        router_card
    ],
    w="60vw",
)
