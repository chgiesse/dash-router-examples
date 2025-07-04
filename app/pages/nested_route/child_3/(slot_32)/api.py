import asyncio

from ..models import QueryParams


async def endpoint(veggie: str = None, **kwargs):
    # filters = QueryParams(**kwargs)
    await asyncio.sleep(0.8)
    data = [
        {"product": "Apples", "sales_january": 120, "sales_february": 100},
        {"product": "Oranges", "sales_january": 98, "sales_february": 90},
        {"product": "Tomatoes", "sales_january": 86, "sales_february": 70},
        {"product": "Grapes", "sales_january": 99, "sales_february": 80},
        {"product": "Bananas", "sales_january": 85, "sales_february": 120},
        {"product": "Lemons", "sales_january": 65, "sales_february": 150},
    ]

    if veggie:
        data = list(
            filter(
                lambda row: row if row.get("product") != veggie.title() else None,
                data,
            )
        )

    return data
