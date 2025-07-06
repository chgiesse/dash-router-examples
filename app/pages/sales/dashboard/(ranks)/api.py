from api.sql_operator import db_operator
from api.models.amazon import AmazonProduct
from api.redis_cache import redis_lru_cache
from ..models import AmazonQueryParams, sales_variant_type, SalesCallbackParams
from ..api import get_agg_variant_column, apply_amazon_filters

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
import pandas as pd
from aiocache import cached
import asyncio


NAMESPACE = "example-dashboard"
TTL = 60 * 5


async def endpoint(**kwargs) -> pd.DataFrame:
    variant = kwargs.pop("variant", SalesCallbackParams.get_default_variant())
    filters = AmazonQueryParams(**kwargs)
    source = (
        get_product_metrics(filters)
        if filters.is_single_view
        else get_category_ranks(filters, variant)
    )
    return await source


# @cached(ttl=30)
@db_operator(timeout=0.5, max_retries=3, verbose=True)
async def get_category_ranks(
    db: AsyncSession,
    filters: AmazonQueryParams,
    variant: sales_variant_type,
) -> pd.DataFrame:
    agg_col = get_agg_variant_column(variant)
    query = select(AmazonProduct.MainCategory, agg_col.label("ProductCount"))

    query = apply_amazon_filters(query, filters)
    query = query.group_by(AmazonProduct.MainCategory)
    query = query.order_by(desc("ProductCount"))
    result = await db.execute(query)
    await asyncio.sleep(1.2)
    return pd.DataFrame(result)


# @cached(ttl=30)
@db_operator(verbose=True)
async def get_product_metrics(db: AsyncSession, filters: AmazonQueryParams):
    await asyncio.sleep(1.5)
    query = select(
        AmazonProduct.MainCategory,
        func.count(AmazonProduct.ProductId).label("ProductCount"),
        func.sum(AmazonProduct.ActualPrice).label("TotalPrice"),
        func.avg(AmazonProduct.DiscountPercentage).label("AvgDiscount"),
    )
    query = apply_amazon_filters(query, filters)
    query = query.group_by(AmazonProduct.MainCategory)
    result = await db.execute(query)
    data = pd.DataFrame(result)
    return data
