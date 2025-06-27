from aiocache import cached
from time import sleep


# @cached(ttl=120)
def endpoint(page: int = 1, *args, **kwargs):
    sleep(1.1)
    page = int(page)
    elements = [
        {
            "invoice_id": 1 * page,
            "mass": "Amazon",
            "symbol": "2025-01-01",
            "amount": 600,
            "action": f"/sales/invoices/{1 * page}",
        },
        {
            "invoice_id": 2 * page,
            "mass": "Apple",
            "symbol": "2025-01-01",
            "amount": 430,
            "action": f"/sales/invoices/{2 * page}",
        },
        {
            "invoice_id": 3 * page,
            "mass": "Nvidia",
            "symbol": "2025-01-01",
            "amount": 130,
            "action": f"/sales/invoices/{3 * page}",
        },
        {
            "invoice_id": 4 * page,
            "mass": "AMD",
            "symbol": "2025-01-01",
            "amount": 275,
            "action": f"/sales/invoices/{4 * page}",
        },
        {
            "invoice_id": 5 * page,
            "mass": "Microsoft",
            "symbol": "2025-01-01",
            "amount": 400,
            "action": f"/sales/invoices/{5 * page}",
        },
    ]

    return elements
