from .components import CategoryRankGraph, create_total_sales_card
from ..models import AmazonQueryParams

import pandas as pd


def layout(data: pd.DataFrame, **kwargs):
    filters = AmazonQueryParams(**kwargs)
    return (
        create_total_sales_card(data=data, category=filters.categories[0])
        if filters.is_single_view
        else CategoryRankGraph(data)
    )
