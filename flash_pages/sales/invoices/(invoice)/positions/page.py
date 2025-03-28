import dash_mantine_components as dmc
from typing import List, Dict


async def layout(data: List[Dict[str, any]] = [], **kwargs):
    return dmc.Stack(
        [
            dmc.Title(
                f"All positions for invoice id: {kwargs.get('invoice_id')}", order=3
            ),
            dmc.DonutChart(
                data=data,
                size=200,
                thickness=30,
                m="auto",
                tooltipDataSource="segment",
                pieProps={
                    "isAnimationActive": True,
                    "animationDuration": 500,
                    "animationEasing": "ease-in-out",
                },
                withLabels=True,
            )
        ]
    )
