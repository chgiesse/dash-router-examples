from ..components import create_invoice_table


async def layout(data, **kwargs):
    return create_invoice_table(data=data)
