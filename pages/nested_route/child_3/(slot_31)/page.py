from typing import Dict, List

import dash_mantine_components as dmc

from ..models import QueryParams


async def layout(data: List[Dict[str, str | int]], *args, **kwargs):
    params = QueryParams(**kwargs)
    return dmc.Box(
        children=[
            dmc.Title("Slot 1 - Child 3", order=3),
            dmc.DonutChart(
                data=data,
                m="auto",
                paddingAngle=3,
                withLabels=True,
                withLabelsLine=False,
                pieProps={
                    "isAnimationActive": True,
                    "animationDuration": 500,
                },
                thickness=15,
                size=220,
            ),
        ],
        # h=300,
        className="fade-in",
    )
