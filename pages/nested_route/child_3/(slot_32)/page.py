from typing import Dict, List

import dash_mantine_components as dmc

from ..models import QueryParams


async def layout(data: List[Dict[str, int | float]], *args, **kwargs):
    filters = QueryParams(**kwargs)
    return dmc.Box(
        children=[
            dmc.Title("Slot 2 - Child 3", order=3),
            dmc.RadarChart(
                h=300,
                data=data,
                dataKey="product",
                withPolarRadiusAxis=True,
                radarProps={
                    "isAnimationActive": True,
                    "animationDuration": 500,
                },
                series=[
                    {"name": "sales_january", "color": "violet.6", "opacity": 0.1},
                    {"name": "sales_february", "color": "violet.3", "opacity": 0.1},
                ],
            ),
        ]
    )
