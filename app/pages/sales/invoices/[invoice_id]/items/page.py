import dash_mantine_components as dmc


async def layout(data, **kwargs):
    invoice_id = kwargs.get("invoice_id")
    return dmc.Stack(
        [
            dmc.Title(
                f"All items for invoice id: {invoice_id}",
                order=3,
                className="fade-in-chart",
            ),
            dmc.BarChart(
                h=300,
                data=data,
                dataKey="item",
                type="waterfall",
                series=[{"name": "Effective tax rate in %", "color": "violet"}],
                withLegend=True,
                barProps={"isAnimationActive": True},
                gridAxis="none",
            ),
        ]
    )
