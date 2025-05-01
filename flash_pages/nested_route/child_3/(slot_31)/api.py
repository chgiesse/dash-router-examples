import asyncio

from ..models import QueryParams


async def endpoint(country: str = None, **kwargs):
    filters = QueryParams(**kwargs)
    await asyncio.sleep(1.3)
    data = [
        {"name": "Usa", "value": 400, "color": "violet.9"},
        {"name": "India", "value": 300, "color": "violet.7"},
        {"name": "Japan", "value": 100, "color": "violet.5"},
        {"name": "Other", "value": 200, "color": "violet.3"},
    ]

    if country:
        data = list(
            filter(
                lambda row: row if row.get("name") != country.title() else None,
                data,
            )
        )

    return data
