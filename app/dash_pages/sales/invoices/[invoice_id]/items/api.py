import random
from time import sleep


def endpoint(**kwargs):
    invoice_id = kwargs.get("invoice_id")
    if invoice_id == str(1):
        1 / 0
    sleep(0.7)
    water_data = [
        {
            "item": "TaxRate",
            "Effective tax rate in %": random.randint(-5, 15),
            "color": "violet.3",
        },
        {
            "item": "Foreign inc.",
            "Effective tax rate in %": random.randint(-5, 15),
            "color": "teal.3",
        },
        {"item": "Perm. diff.", "Effective tax rate in %": -3, "color": "teal"},
        {
            "item": "Credits",
            "Effective tax rate in %": random.randint(-5, 15),
            "color": "teal.3",
        },
        {"item": "Loss carryf.", "Effective tax rate in %": -2, "color": "teal"},
        {
            "item": "Law changes",
            "Effective tax rate in %": random.randint(-5, 15),
            "color": "indigo.3",
        },
        {"item": "Reven. adj.", "Effective tax rate in %": 4, "color": "red"},
        {
            "item": "ETR",
            "Effective tax rate in %": 3.5,
            "color": "blue.3",
            "standalone": True,
        },
    ]
    return water_data
