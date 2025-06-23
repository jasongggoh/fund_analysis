import os
import pandas as pd

from src.utils.file_handler import FileHandler
from src.models.external_fund import external_fund_schema, col_rename_dict
from src.utils.common import parse_date_cols, PROJECT_ROOT
from src.utils.database_utils import validate_schema

class ExternalFundsRepo:

    def __init__(self):
        super().__init__()
        self.data = None
        self.date_cols = ["data_date"]
        self.col_rename_dict = col_rename_dict

        self.initialise_data()

    def initialise_data(self) -> None:
        mappings = FileHandler.initialize_file_mapping(os.path.join(PROJECT_ROOT, r"src/repositories/file_mapping/file_mapping_config.yml"))
        data = FileHandler.load_files(file_mappings=mappings, config_dir=os.path.join(PROJECT_ROOT, "external-funds"))

        self.data : pd.DataFrame = data
        self.data.rename(columns=self.col_rename_dict, inplace=True)

        if self.data.empty:
            raise RuntimeError("No data loaded from file.")

    def fetch(self, financial_type_filter: str = None) -> pd.DataFrame:
        data = validate_schema(self.data, external_fund_schema)
        if not financial_type_filter:
            return data

        return data[data["financial_type"] == financial_type_filter]

    def fetch_all_equities_as_df(self) -> pd.DataFrame:
        data = self.fetch(financial_type_filter="Equities", )
        return parse_date_cols(data, self.date_cols)

