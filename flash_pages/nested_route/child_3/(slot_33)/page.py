from typing import List, Dict
import dash_mantine_components as dmc


async def layout(data: List[Dict[str, str | int]], *args, **kwargs):
    return dmc.Box(
        [
            dmc.Title("Slot - 3 of Child - 3", order=3, mb="md"),
            dmc.Stack(
                [
                    dmc.Text("Apples sales:", mb="md", pl="md"),
                    dmc.CompositeChart(
                        h=180,
                        data=data,
                        dataKey="date",
                        series=[
                            {"name": "Apples", "color": "violet.6", "type": "area"}
                        ],
                        composedChartProps={"syncId": "groceries"},
                        areaProps={
                            "isAnimationActive": True,
                            "animationDuration": 500,
                            "animationEasing": "ease-in-out",
                        },
                    ),
                    dmc.Text("Tomatoes sales:", mb="md", pl="md", mt="xl"),
                    dmc.CompositeChart(
                        h=180,
                        data=data,
                        dataKey="date",
                        series=[
                            {"name": "Tomatoes", "color": "violet.3", "type": "bar"}
                        ],
                        composedChartProps={"syncId": "groceries"},
                        barProps={"isAnimationActive": True},
                    ),
                ]
            ),
        ],
        # withBorder=True,
        className="FadeInRow",
    )
