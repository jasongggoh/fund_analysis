import os
import pandas as pd

from typing import List

from src.utils.file_handler import FileHandler
from src.models.external_fund import ExternalFund
from src.utils.common import parse_date_cols, PROJECT_ROOT


def _parse_external_funds(df: pd.DataFrame) -> List[ExternalFund]:
    funds = df.to_dict("records")

    return [
        ExternalFund(
            financial_type=item.get("financial type"),
            symbol=item.get("symbol"),
            security_name=item.get("security name"),
            sedol=item.get("sedol"),
            price=item.get("price"),
            quantity=item.get("quantity"),
            realised_pnl=item.get("realised p/l"),
            market_value=item.get("market value"),
            fund_name=item.get("fund name"),
            data_date=item.get("data date")
        ) for item in funds
    ]


class ExternalFundsRepo:

    def __init__(self):
        super().__init__()
        self.data = None
        self.date_cols = ["data_date"]

        self.initialise_data()

    def initialise_data(self) -> None:
        mappings = FileHandler.initialize_file_mapping(os.path.join(PROJECT_ROOT, r"src/repositories/file_mapping/file_mapping_config.yml"))
        data = FileHandler.load_files(file_mappings=mappings, config_dir=os.path.join(PROJECT_ROOT, "external-funds"))

        self.data = data

    def fetch_all(self) -> List[ExternalFund]:
        data = self.fetch_all_raw()

        return _parse_external_funds(data)

    def fetch_all_equities(self) -> List[ExternalFund]:
        data = self.fetch_all_raw()
        equities_df = data[data["financial type"] == "Equities"]

        return _parse_external_funds(equities_df)

    def fetch_all_equities_as_df(self) -> pd.DataFrame:
        funds_data = self.fetch_all_equities()
        fund_df = pd.DataFrame(data.model_dump() for data in funds_data)
        fund_df = parse_date_cols(fund_df, self.date_cols)

        return fund_df if not fund_df.empty else pd.DataFrame()

    def fetch_all_raw(self) -> pd.DataFrame:
        # convert pd.NaN to None first before parsing
        return self.data.where(pd.notnull(self.data), None)

