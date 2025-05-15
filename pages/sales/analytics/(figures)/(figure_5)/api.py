import plotly.express as px
from aiocache import cached
import asyncio


@cached(ttl=30)
async def endpoint(*args, **kwargs):
    await asyncio.sleep(1)
    return dict(
        labels=[
            "Eve",
            "Cain",
            "Seth",
            "Enos",
            "Noam",
            "Abel",
            "Awan",
            "Enoch",
            "Azura",
        ],
        parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"],
        values=[10, 14, 12, 10, 2, 6, 6, 4, 4],
    )
