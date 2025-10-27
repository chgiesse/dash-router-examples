from .components.actionbar import ActionBar
from .components.menu import GraphDownload
from .models import AmazonQueryParams

import dash_mantine_components as dmc


def layout(
    ranks=None,
    revenue=None,
    sentiment=None,
    filters: AmazonQueryParams = None,
    **kwargs
):

    filters = AmazonQueryParams(**kwargs)

    return [
        GraphDownload(),
        dmc.Grid(
            [
                dmc.GridCol(
                    span={"xl": 9, "lg": 9, "md": 9, "sm": 12, "xs": 12, "xxs": 12}, # type: ignore
                    order={"xl": 1, "lg": 1, "md": 1, "sm": 2, "xs": 2, "xxs": 2}, # type: ignore
                    children=dmc.Grid(
                        [
                            dmc.GridCol(
                                ranks,
                                span=12 if filters.is_single_view else 4,
                            ),
                            dmc.GridCol(
                                revenue,
                                span=12 if filters.is_single_view else 8,
                            ),
                            dmc.GridCol(
                                sentiment,
                                span=12,
                            ),
                        ]
                    ),
                ),
                dmc.GridCol(
                    span={"xl": 3, "lg": 3, "md": 3, "sm": 12, "xs": 12, "xxs": 12}, # type: ignore
                    order={"xl": 2, "lg": 2, "md": 2, "sm": 1, "xs": 1, "xxs": 1}, # type: ignore
                    # pos="sticky",
                    # top=0,
                    # h="calc(100vh - var(--mantine-spacing-xl))",
                    # bg="var(--mantine-color-body)",
                    children=[
                        dmc.Title("Example Dashboard", order=2, ml="md"),
                        ActionBar(filters),
                    ],
                ),
            ]
        ),
    ]
