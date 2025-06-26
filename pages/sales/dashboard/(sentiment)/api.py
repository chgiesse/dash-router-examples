from api.sql_operator import db_operator
from api.models.amazon import AmazonProduct
from api.redis_cache import redis_lru_cache
from ..models import AmazonQueryParams
from ..api import apply_amazon_filters, get_date_granularity_column

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import pandas as pd
import asyncio
from aiocache import cached

NAMESPACE = "example-dashboard"
TTL = 60 * 5


class SentimentEndpointResult(BaseModel):
    sentiment_data: pd.DataFrame
    rating_data: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True


async def endpoint(filters: AmazonQueryParams = None, **kwargs) -> pd.DataFrame:
    filters = AmazonQueryParams(**kwargs)
    sentiment_data, rating_data = await asyncio.gather(
        get_total_sentiment(filters=filters), get_avg_rating(filters=filters)
    )

    return SentimentEndpointResult(
        sentiment_data=sentiment_data, rating_data=rating_data
    )


# @cached(ttl=120)
@db_operator(verbose=True)
async def get_total_sentiment(db: AsyncSession, filters: AmazonQueryParams):
    date_col, _ = get_date_granularity_column(
        filters.granularity, AmazonProduct.SaleDate
    )
    query = select(
        date_col.label("Date"),
        AmazonProduct.ReviewSentiment,
        func.count(AmazonProduct.ProductId).label("ProductCount"),
    )

    query = apply_amazon_filters(query, filters)
    query = query.group_by(date_col, AmazonProduct.ReviewSentiment)
    result = await db.execute(query)

    data = pd.DataFrame(result)
    data = data.pivot(columns="ReviewSentiment", index="Date", values="ProductCount")
    data = data.fillna(0)
    await asyncio.sleep(1.2)
    return data


# @cached(ttl=120)
@db_operator(verbose=True)
async def get_avg_rating(db: AsyncSession, filters: AmazonQueryParams):
    await asyncio.sleep(1.2)
    date_col, _ = get_date_granularity_column(
        filters.granularity, AmazonProduct.SaleDate
    )
    query = select(
        date_col.label("Date"), func.avg(AmazonProduct.Rating).label("AvgRating")
    )

    query = apply_amazon_filters(query, filters)
    query = query.group_by(date_col)
    result = await db.execute(query)
    data = pd.DataFrame(result)
    data.set_index("Date", inplace=True)
    data.sort_index(ascending=True, inplace=True)
    return data
