from time import sleep

from .._components.table import create_invoice_table


def layout(**kwargs):
    sleep(1.3)
    return create_invoice_table()
