from ..components import create_invoice_table


async def layout(data, page: int = None, **kwargs):
    return create_invoice_table(data=data, page=page)
