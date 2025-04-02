from aiocache import cached
import asyncio

# @cached(ttl=120)
async def endpoint(*args, **kwargs):
    await asyncio.sleep(1.1)
    elements = [
        {
            "invoice_id": 1,
            "mass": "Amazon",
            "symbol": "2025-01-01",
            "amount": 600,
            "action": "/sales/invoices/1",
        },
        {
            "invoice_id": 2,
            "mass": "Apple",
            "symbol": "2025-01-01",
            "amount": 430,
            "action": "/sales/invoices/2",
        },
        {
            "invoice_id": 3,
            "mass": "Nvidia",
            "symbol": "2025-01-01",
            "amount": 130,
            "action": "/sales/invoices/3",
        },
        {
            "invoice_id": 4,
            "mass": "AMD",
            "symbol": "2025-01-01",
            "amount": 275,
            "action": "/sales/invoices/4",
        },
        {
            "invoice_id": 5,
            "mass": "Microsoft",
            "symbol": "2025-01-01",
            "amount": 400,
            "action": "/sales/invoices/5",
        },
    ]

    return elements