import dash_mantine_components as dmc


def layout(test_1=None, test_2=None, **kwargs):
    return dmc.Title(f"OM Overview {test_1} {test_2}")
