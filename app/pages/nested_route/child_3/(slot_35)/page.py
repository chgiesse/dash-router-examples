from typing import Dict, List

import dash_mantine_components as dmc

from ..models import QueryParams


async def layout(data: List[Dict[str, str | int]], *args, **kwargs):
    filters = QueryParams(**kwargs)
    return dmc.Box(
        [
            dmc.Title("Slot - 5 of Child - 3", order=3),
            dmc.CompositeChart(
                h=300,
                data=data,
                dataKey="date",
                withLegend=True,
                maxBarWidth=30,
                areaProps={
                    "isAnimationActive": True,
                    "animationDuration": 500,
                    "animationEasing": "ease-in-out",
                },
                barProps={"isAnimationActive": True},
                series=[
                    {
                        "name": "Tomatoes",
                        "color": "blue.2",
                        "type": "bar",
                    },
                    {"name": "Apples", "color": "orange.4", "type": "line"},
                    {"name": "Oranges", "color": "blue.8", "type": "area"},
                ],
            ),
        ],
        h=400,
        className="fade-in",
    )
