from ..components import create_invoice_table


def layout(data, page: int = None, **kwargs):
    print("kwargs: ", kwargs, flush=True)
    return create_invoice_table(data=data, page=page)
