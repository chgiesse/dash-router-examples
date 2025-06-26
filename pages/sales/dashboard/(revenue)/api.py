from api.sql_operator import db_operator
from api.models.amazon import AmazonProduct
from api.redis_cache import redis_lru_cache
from ..models import AmazonQueryParams, SalesCallbackParams
from ..api import (
    apply_amazon_filters,
    get_date_granularity_column,
    get_agg_variant_column,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import pandas as pd
from aiocache import cached
import asyncio

NAMESPACE = "example-dashboard"
TTL = 60 * 5


# @cached(ttl=TTL)
@db_operator(verbose=True)
async def endpoint(db: AsyncSession, **kwargs):
    await asyncio.sleep(1.2)
    variant = kwargs.pop("variant", SalesCallbackParams.get_default_variant())
    filters = AmazonQueryParams(**kwargs)
    agg_col = get_agg_variant_column(variant)
    date_col, _ = get_date_granularity_column(
        filters.granularity, AmazonProduct.SaleDate
    )
    query = select(
        AmazonProduct.MainCategory,
        date_col.label("Date"),
        agg_col.label("ProductCount"),
    )

    query = apply_amazon_filters(query, filters)
    query = query.group_by(date_col, AmazonProduct.MainCategory)
    query = query.order_by(desc("ProductCount"))
    result = await db.execute(query)
    data = pd.DataFrame(result)
    data = data.pivot(index="Date", columns="MainCategory", values="ProductCount")
    data = data.fillna(0)
    return data
