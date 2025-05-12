import datetime
from pydantic import BaseModel, field_validator


class EquityPrice(BaseModel):
    reference_date: datetime.date
    symbol: str
    reference_price: float

    @field_validator("reference_date", mode="before") # noqa
    # pycharm type checking issue - field validator already returns a class method
    @classmethod
    def parse_date(cls, v: str) -> datetime.date:
        if isinstance(v, str):
            return datetime.datetime.strptime(v, "%m/%d/%Y").date()
        raise ValueError(f"Incorrect date format: {str(v)}")