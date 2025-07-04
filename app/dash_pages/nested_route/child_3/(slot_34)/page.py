import dash_mantine_components as dmc


def layout(*args, **kwargs):
    1 / 0
    return dmc.Card(
        dmc.Title("Slot - 4 of Child - 3", order=3),
        h=400,
        withBorder=True,
        className="fade-in",
    )
