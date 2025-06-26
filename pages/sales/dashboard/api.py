from api.models.amazon import AmazonProduct
from .models import AmazonQueryParams, sales_variant_type, granularity_type

from sqlalchemy import func
from sqlalchemy.orm import Query


def apply_amazon_filters(query: Query, filters: AmazonQueryParams):

    query = query.filter(AmazonProduct.MainCategory.in_(filters.get_categroies()))

    if len(filters.categories) > 0:
        query = query.filter(AmazonProduct.MainCategory.in_(filters.categories))

    if date_range := filters.sale_date_range:
        query = query.filter(
            AmazonProduct.SaleDate.between(cleft=date_range[0], cright=date_range[1])
        )

    if rating := filters.rating_range:
        query = query.filter(
            AmazonProduct.Rating.between(cleft=rating[0], cright=rating[1])
        )

    if filters.sentiment:
        query = query.filter(AmazonProduct.ReviewSentiment.in_(filters.sentiment))

    return query


def get_agg_variant_column(agg_variant: sales_variant_type):
    if agg_variant == "amount":
        return func.count(AmazonProduct.ProductId)

    if agg_variant == "discount":
        return func.avg(AmazonProduct.DiscountPercentage)

    if agg_variant == "price":
        return func.sum(AmazonProduct.ActualPrice)


def get_date_granularity_column(granularity: granularity_type, date_column):
    if granularity == "quarter":
        return func.to_char(date_column, 'YYYY-"Q"Q'), "quarter"
    elif granularity == "month":
        return func.to_char(date_column, "YYYY-MM"), "month"
    elif granularity == "year":
        return func.to_char(date_column, "YYYY"), "year"
    else:
        return func.to_char(date_column, "YYYY-MM"), "month"
