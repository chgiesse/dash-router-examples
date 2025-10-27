import dash_mantine_components as dmc
from .components import TestComponentStream
from ..feed_component.page import layout as FeedComponentLayout


async def layout(*args, **kwargs):
    return dmc.Grid([
        dmc.GridCol(
            TestComponentStream(),
            span={
                "xxl": 8,
                "xl": 8,
                "lg": 8,
                "md": 12,
                "sm": 12,
                "xs": 12,
                "xxs": 12
            },  # type: ignore
            order={
                "xxl": 1,
                "xl": 1,
                "lg": 1,
                "md": 2,
                "sm": 2,
                "xs": 2,
                "xxs": 2
            } # type: ignore
        ),
        dmc.GridCol(
            await FeedComponentLayout(),
            span={
                "xxl": 4,
                "xl": 4,
                "lg": 4,
                "md": 12,
                "sm": 12,
                "xs": 12,
                "xxs": 12
            }, # type: ignore
            order={
                "xxl": 2,
                "xl": 2,
                "lg": 2,
                "md": 1,
                "sm": 1,
                "xs": 1,
                "xxs": 1
            } # type: ignore
        ),
    ],
    gutter="lg"
    )
