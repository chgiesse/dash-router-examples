import dash_mantine_components as dmc


def layout(*args, **kwargs):
    data = [
        {"month": "January", "Smartphones": 1200, "Laptops": 900, "Tablets": 200},
        {"month": "February", "Smartphones": 1900, "Laptops": 1200, "Tablets": 400},
        {"month": "March", "Smartphones": 400, "Laptops": 1000, "Tablets": 200},
        {"month": "April", "Smartphones": 1000, "Laptops": 200, "Tablets": 800},
        {"month": "May", "Smartphones": 800, "Laptops": 1400, "Tablets": 1200},
        {"month": "June", "Smartphones": 750, "Laptops": 600, "Tablets": 1000},
    ]

    return dmc.Box(
        [
            dmc.Title("Slot 2", order=3, my="sm"),
            dmc.BarChart(
                h=300,
                dataKey="month",
                data=data,
                withLegend=True,
                barProps={
                    "isAnimationActive": True,
                    "animationDuration": 500,
                },
                series=[
                    {"name": "Smartphones", "color": "violet.6"},
                    {"name": "Laptops", "color": "violet.3"},
                    {"name": "Tablets", "color": "violet.1"},
                ],
            ),
        ],
        # h=400,
        # withBorder=True,
    )
