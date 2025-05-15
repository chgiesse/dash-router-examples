import dash_mantine_components as dmc


async def layout(*args, **kwargs):
    data = [
        {"date": "Mar 22", "Apples": 2890, "Oranges": 2338, "Tomatoes": 2452},
        {"date": "Mar 23", "Apples": 2756, "Oranges": 2103, "Tomatoes": 2402},
        {"date": "Mar 24", "Apples": 3322, "Oranges": 986, "Tomatoes": 1821},
        {"date": "Mar 25", "Apples": 3470, "Oranges": 2108, "Tomatoes": 2809},
        {"date": "Mar 26", "Apples": 3129, "Oranges": 1726, "Tomatoes": 2290},
    ]
    return dmc.Box(
        [
            dmc.Title("Slot 1", order=3, my="sm"),
            dmc.AreaChart(
                h=300,
                dataKey="date",
                data=data,
                withLegend=True,
                areaProps={
                    "isAnimationActive": True,
                    "animationDuration": 500,
                },
                series=[
                    {"name": "Oranges", "color": "violet.9"},
                    {"name": "Apples", "color": "violet.3"},
                    {"name": "Tomatoes", "color": "violet.6"},
                ],
                curveType="linear",
                tickLine="xy",
                withGradient=True,
                withXAxis=True,
            ),
        ],
        # h=400,
        # withBorder=True,
    )
