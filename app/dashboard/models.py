# from pydantic import BaseModel, Field, field_validator
# from typing import List, Literal, get_args
# from datetime import date, timedelta
# import json


# sales_variant_type = Literal["amount", "price", "discount"]

# granularity_type = Literal["year", "quarter", "month"]


# class AmazonQueryParams(BaseModel):
#     categories: List[
#         Literal[
#             "Computers&Accessories",
#             "Electronics",
#             # "MusicalInstruments",
#             "OfficeProducts",
#             "Home&Kitchen",
#             # "HomeImprovement",
#             # "Toys&Games",
#             # "Car&Motorbike",
#             # "Health&PersonalCare",
#             # "Sports",
#         ]
#         | None
#     ] = []

#     sale_date_range: List[date] = Field(
#         default_factory=lambda: [date.today() - timedelta(days=365 * 2), date.today()]
#     )

#     rating_range: List[float] = Field(default_factory=lambda: [0.0, 5.0])

#     granularity: granularity_type = Field(default="month")

#     sentiment: List[Literal["positive", "neutral", "negative"] | None] = []

#     @field_validator(
#         "categories", "sale_date_range", "rating_range", "sentiment", mode="before"
#     )
#     @classmethod
#     def parse_json_string(cls, value):
#         if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
#             try:
#                 parsed_value = json.loads(value)
#                 return parsed_value
#             except json.JSONDecodeError:
#                 pass
#         return value

#     @classmethod
#     def get_categroies(cls):
#         cat_annotations = list(cls.__annotations__["categories"].__args__)
#         cat_values = [val for val in get_args(cat_annotations[0])][0].__args__
#         return cat_values

#     @classmethod
#     def get_sentiments(cls):
#         cat_annotations = list(cls.__annotations__["sentiment"].__args__)
#         cat_values = [val for val in get_args(cat_annotations[0])][0].__args__
#         return cat_values

#     @classmethod
#     def get_granularities(cls):
#         return list(cls.__annotations__["granularity"].__args__)

#     @classmethod
#     def get_rating_range(cls):
#         return cls.model_fields["rating_range"].default_factory()

#     @property
#     def is_single_view(self):
#         return len(self.categories) == 1

#     @property
#     def is_default(self) -> bool:

#         if self.categories != []:
#             return False

#         default_date_range = self.__class__.model_fields[
#             "sale_date_range"
#         ].default_factory()
#         if self.sale_date_range != default_date_range:
#             return False

#         if self.rating_range != self.__class__.get_rating_range():
#             return False

#         if self.granularity != "month":
#             return False

#         return True


# class SalesCallbackParams(BaseModel):
#     variant: sales_variant_type = Field(default="amount")
#     is_relative: bool | None = None
#     is_running: bool | None = None

#     @classmethod
#     def get_variants(cls):
#         return list(cls.__annotations__["variant"].__args__)

#     @classmethod
#     def get_default_variant(cls):
#         return cls.model_fields["variant"].default
