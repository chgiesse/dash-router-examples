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

NAMESPACE = "example-dashboard"
TTL = 60 * 5


class SentimentEndpointResult(BaseModel):
    sentiment_data: pd.DataFrame
    rating_data: pd.DataFrame

    class Config:
        arbitrary_types_allowed=True


async def endpoint(**kwargs) -> pd.DataFrame:
    print('HAAAAAALLLLLLOLOOOOO', flush=True)
    filters = AmazonQueryParams(**kwargs)
    sentiment_data, rating_data = await asyncio.gather(
        get_total_sentiment(filters=filters), get_avg_rating(filters=filters)
    )

    return SentimentEndpointResult(sentiment_data, rating_data)


@db_operator(verbose=True)
# @redis_lru_cache.cache(namespace=NAMESPACE, ttl=TTL)
async def get_total_sentiment(db: AsyncSession, filters: AmazonQueryParams):
    await asyncio.sleep(0.6)
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
    return data


@db_operator(verbose=True)
# @redis_lru_cache.cache(namespace=NAMESPACE, ttl=TTL)
async def get_avg_rating(db: AsyncSession, filters: AmazonQueryParams):
    await asyncio.sleep(0.6)
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
