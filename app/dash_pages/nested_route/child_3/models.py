from pydantic import BaseModel, field_validator, ValidationError, Field
from typing import List, Literal, get_type_hints, Literal, get_args
import typing
from datetime import date, timedelta


class QueryParams(BaseModel):
    veggie: (
        Literal["oranges", "apples", "lemons", "bananas", "tomatoes", "grapes"] | None
    ) = None

    country: (
        Literal[
            "japan",
            "usa",
            "other",
            "india",
        ]
        | None
    ) = None

    period: List[str | date | None] = []

    @field_validator("period", mode="before")
    def validate_period(cls, value):

        if not value:
            return []

        if isinstance(value, str) and ", " in value:
            return value.split(", ")

        if isinstance(value, List):
            if len(value) == 2:
                return value

        raise ValidationError(f"Value {value} with type {type(value)} is not allowed.")

    @property
    def is_empty(self):
        return self.veggie is None and self.country is None and len(self.period) == 0

    def get_literals(self, attr_name: str) -> List[str]:
        type_hints = get_type_hints(self.__class__)

        if attr_name not in type_hints:
            return []

        type_annotation = type_hints[attr_name]
        args = get_args(type_annotation)

        literal_type = None
        for arg in args:
            origin = typing.get_origin(arg)
            if origin is Literal:
                literal_type = arg
                break

        if literal_type is None:
            return []

        return list(get_args(literal_type))
