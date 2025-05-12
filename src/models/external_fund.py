import datetime

from pydantic import BaseModel

class ExternalFund(BaseModel):
    financial_type: str | None
    symbol: str | None
    security_name: str | None
    sedol: str | None
    price: float | None
    quantity: float | None
    realised_pnl: float | None
    market_value: float | None
    fund_name: str
    data_date: datetime.date