from pydantic import BaseModel

class EquityReference(BaseModel):
    symbol: str | None
    country: str | None
    security_name: str | None
    sector: str | None
    industry: str | None
    currency: str | None