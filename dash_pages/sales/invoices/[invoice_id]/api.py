
from time import sleep

import random


def endpoint(invoice_id: int, **kwargs):
    if not invoice_id:
        return None

    sleep(0.9)

    data_comp = [
        {
            "date": "Mar 22",
            "Apples": random.randint(50, 3000),
            "Oranges": random.randint(50, 3000),
            "Tomatoes": 2452,
        },
        {
            "date": "Mar 23",
            "Apples": 2756,
            "Oranges": 2103,
            "Tomatoes": 2402,
        },
        {
            "date": "Mar 24",
            "Apples": 3322,
            "Oranges": random.randint(50, 3000),
            "Tomatoes": 1821,
        },
        {
            "date": "Mar 25",
            "Apples": random.randint(50, 3000),
            "Oranges": random.randint(50, 3000),
            "Tomatoes": 2809,
        },
        {
            "date": "Mar 26",
            "Apples": 3129,
            "Oranges": random.randint(50, 3000),
            "Tomatoes": random.randint(50, 3000),
        },
    ]
    return data_comp
