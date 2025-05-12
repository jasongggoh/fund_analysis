from typing import override, List

import pandas as pd

from src.repositories.price_repo import PriceRepo
from src.models.equity_price import EquityPrice
from src.utils.common import parse_date_cols


class EquityPriceRepo(PriceRepo):
    def __init__(self):
        super().__init__()
        self.table_name = "equity_prices"
        self.date_cols = ["reference_date"]

    @override
    def fetch_all(self) -> List[EquityPrice]:
        data = super().select_all_data(self.table_name)

        return [
            EquityPrice(
                reference_date=item.get("datetime"),
                symbol=item.get("symbol"),
                reference_price=item.get("price")
            ) for item in data
        ]

    @override
    def fetch_all_as_df(self) -> pd.DataFrame:
        price_data = self.fetch_all()
        price_data_df = pd.DataFrame(data.model_dump() for data in price_data)
        price_data_df = parse_date_cols(price_data_df, self.date_cols)

        return price_data_df if not price_data_df.empty else pd.DataFrame()