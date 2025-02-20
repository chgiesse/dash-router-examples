import dash_mantine_components as dmc

card = dmc.Card(
    className="animate-fade-in",
    children=[
        dmc.CardSection(
            dmc.Image(
                src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/images/bg-8.png",
                h=160,
                alt="Norway",
            )
        ),
        dmc.Group(
            [
                dmc.Text("Norway Fjord Adventures", fw=500),
                dmc.Badge("On Sale", color="pink"),
            ],
            justify="space-between",
            mt="md",
            mb="xs",
        ),
        dmc.Text(
            "With Fjord Tours you can explore more of the magical fjord landscapes with tours and activities on and "
            "around the fjords of Norway",
            size="sm",
            c="dimmed",
        ),
        dmc.Anchor(
            dmc.Button(
                "Book classic tour now",
                fullWidth=True,
                mt="md",
                radius="md",
            ),
            href="/sales/analytics",
            underline=False,
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    w=330,
)
