from aiocache import cached
import asyncio

import random


# @cached(ttl=120)
async def endpoint(invoice_id: int, **kwargs):

    print("invoice_id", invoice_id, kwargs, flush=True)

    if not invoice_id:
        return None

    await asyncio.sleep(0.9)

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
