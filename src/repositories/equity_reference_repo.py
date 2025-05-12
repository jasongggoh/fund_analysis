import pandas as pd
from typing import List


from typing_extensions import override

from src.repositories.price_repo import PriceRepo
from src.models.equity_reference import EquityReference
from src.utils.common import parse_date_cols


class EquityReferenceRepo(PriceRepo):

    def __init__(self):
        super().__init__()
        self.table_name = "equity_reference"

    @override
    def fetch_all(self) -> List[EquityReference]:
        data = super().select_all_data(self.table_name)

        return [
            EquityReference(
                symbol=item.get("symbol"),
                country=item.get("country"),
                security_name=item.get("security name"),
                sector=item.get("sector"),
                industry=item.get("industry"),
                currency=item.get("currency")
            ) for item in data
        ]

    @override
    def fetch_all_as_df(self):
        ref_data = self.fetch_all()
        ref_data_df = pd.DataFrame(data.model_dump() for data in ref_data)
        ref_data_df = parse_date_cols(ref_data_df, self.date_cols)

        return ref_data_df